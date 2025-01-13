import os
import logging
import json

from package.database import Database
from gps import Kml
from utils import MifitUtils, Utils


class Standalone:
    def __init__(self, dump_path="", report_path="report.json", start_date=None, end_date=None, gps=None):
        self.dump_path = dump_path
        self.report_path = report_path
        self.start_date = Utils.date_to_timestamp(start_date, "%Y-%m-%d", 0, False)
        self.end_date = Utils.date_to_timestamp(end_date, "%Y-%m-%d", Utils.get_current_timestamp(), False)
        self.gps = gps
        logging.info("Start date: {}".format( self.start_date))
        logging.info("End date: {}".format( self.end_date))
        self.report_struct = {}
        self.kml_struct = Kml()

    def analyse(self):
        
        self.report_struct = {"case":{}, "report":{}}
        self.report_struct["case"]["number"] = os.environ.get("CASE_NUMBER")
        self.report_struct["case"]["examinerName"] = os.environ.get("EXAMINER_NAME")
        self.report_struct["case"]["examinerPhone"] = os.environ.get("EXAMINER_PHONE")
        self.report_struct["case"]["examinerEmail"] = os.environ.get("EXAMINER_EMAIL")
        self.report_struct["case"]["examinerNotes"] = os.environ.get("EXAMINER_NOTES")
        self.report_struct["case"]["caseDate"] = Utils.get_current_timestamp()

        origin_dbs = Utils.list_files(self.dump_path, "origin_db", ["journal", "wal", "-shm", "default"])
        stress_dbs = Utils.list_files(self.dump_path, "stress_", ["journal", "wal", "shm", "default"])
        spo_dbs = Utils.list_files(self.dump_path, "spo2_", ["journal", "wal", "shm", "db-wal"])
        femaleHealth_dbs = Utils.list_files(self.dump_path, "FemaleHealth_", ["journal", "wal", "shm", "db-wal", "xml"])
        #sdk_xmls = Utils.list_files(self.dump_path, "hm_id_sdk_android")

        for db in origin_dbs:
            try:
                self.report_struct["report"]["origin"] = self.__analyze_origin(db)
            except Exception as e:
                logging.warning(e)
                pass
                

        for db in stress_dbs:
            try:
                logging.info("Analysing {} database... ".format(db))
                self.report_struct["report"]["stress"] = self.__analyze_stress(db)
            except Exception as e:
                logging.warning(e)
                pass
        
        for db in spo_dbs:
            try:
                logging.info("Analysing {} database... ".format(db))
                self.report_struct["report"]["spo"] = self.__analyze_spo(db)
                
            except Exception as e:
                logging.warning(e)
                pass
        
        for db in femaleHealth_dbs:
            try:
                self.report_struct["report"]["female"] = self.__analyze_female(db)
            except Exception as e:
                logging.warning(e)
                pass
        
        #for xml_file in sdk_xmls:
        #    try:
        #        logging.info("Analysing {} file... ".format(xml_file))
        #        self.report_struct["report"]["users"] = self.__analyze_sdk(xml_file)
        #    except Exception as e:
        #        logging.warning(e)
        #        pass

        return self.report_struct
        
    def report(self):
        logging.info("Generating report...")
        Utils.write_json(self.report_path, self.report_struct)
        js_report = "var reportRAW = " + json.dumps(self.report_struct, indent = 2)
        file_handler = open(os.path.join("./report/js", "report.js"), "w")
        file_handler.write(js_report)
        file_handler.close()

        if self.gps:
            self.kml_struct.write("map.kml")
            
        logging.info("Full HTML report: {}".format(os.path.abspath(os.path.join("report","index.html"))))
        
    
    @staticmethod
    def detach_report(report, report_path):
        logging.info("Generating detach report...")
        js_report = "var reportRAW = " + json.dumps(report, indent = 2)
        file_handler = open(report_path, "wb")
        file_handler.write(js_report)
        file_handler.close()
        # logging.info("Full HTML report: {}".format(os.path.abspath(os.path.join(os.path.dirname(__file__), "report", "index.html"))))
        return report_path
        



#MIFIT analyse functions
    def __analyze_origin(self, database_path):

        try: 
            database = Database(database_path)
            hr_records = []

            results = database.execute_query(
                "select TIME, HR, DEVICE_ID from HEART_RATE")
            for entry in results:
                hr_record = {}
                try:
                    if(not Utils.is_timestamp_between_timestamps(int(entry[0]), self.start_date, self.end_date)):
                        continue
                    
                    hr_record["time"] = int(entry[0])
                    hr_record["value"] = str(entry[1])
                    hr_record["device"] = str(entry[2])
                    hr_records.append(hr_record)
                except:
                    pass
            results = database.execute_query(
                    "select CALENDAR, ENABLED from ALARM")
            
            alarm_records = []
            for entry in results:
                alarm_record = {}
                try:
                    alarm_record["time"] = int(entry[0])
                    alarm_record["enabled"] = str(entry[1])
                    alarm_records.append(alarm_record)
                except:
                    pass

            results = database.execute_query(
                    "select SOURCE, DATE, SUMMARY, DATA from DATE_DATA")
            
            step_records = []
            for entry in results:
                summary = json.loads(entry[2])
                
                if summary.get("stp") and summary.get("stp").get("stage"):
                    summary = json.loads(entry[2])
                    for summary_record in summary.get("stp").get("stage"):
                        try:
                            # logging.warning(Utils.date_to_timestamp(str(entry[1]), "%Y-%m-%d"))
                            if(not Utils.is_timestamp_between_timestamps(Utils.date_to_timestamp(str(entry[1]), "%Y-%m-%d"), self.start_date, self.end_date)):
                                continue
                            step_record = {}
                            step_record["date"] = str(entry[1])
                            step_record["from"] = Utils.minutes_to_time(summary_record.get("start"))
                            step_record["to"] = Utils.minutes_to_time(summary_record.get("stop"))
                            step_record["mode"] = MifitUtils.mode_to_activity(str(summary_record.get("mode")))
                            step_record["distance"] = str(summary_record.get("dis"))
                            step_record["calories"] = str(summary_record.get("cal"))
                            step_record["steps"] = str(summary_record.get("step"))
                            step_records.append(step_record)
                        except Exception as e:
                            pass
                            logging.warning(e)

                # sleep data
                sleep_records = []
                if summary.get("slp") and summary.get("slp").get("stage"):
                    for summary_record in summary.get("slp").get("stage"):
                        try:
                            if(not Utils.is_timestamp_between_timestamps(Utils.date_to_timestamp(str(entry[1]), "%Y-%m-%d"), self.start_date, self.end_date)):
                                continue
                            sleep_record = {}
                            sleep_record["date"] = str(entry[1])
                            sleep_record["from"] = Utils.minutes_to_time(summary_record.get("start"))
                            sleep_record["to"] = Utils.minutes_to_time(summary_record.get("stop"))
                            sleep_record["mode"] = MifitUtils.mode_to_sleep(str(summary_record.get("mode")))
                            sleep_records.append(sleep_record)
                        except Exception as e:
                            pass
                            logging.warning(e)


            # Workouts
            results = database.execute_query(
                    "select tr.TYPE, tr.DATE, tr.TRACKID, tr.DISTANCE, tr.COSTTIME, tr.CAL, tr.PACE, tr.SFREQ, tr.AVGHR, tr.TOTAL_STEP, tr.ENDTIME, td.BULKLL from TRACKRECORD tr LEFT JOIN TRACKDATA td ON (tr.TRACKID =  td.TRACKID)")
            
            activity_records = []
            
            for entry in results:
                activity_record = {}
                try:
                    activity_record["type"] = MifitUtils.mode_to_workout(str(entry[0]))
                    activity_record["start"] = int(entry[2])
                    activity_record["end"] =  int(entry[10])
                    activity_record["distance"] = str(entry[3])
                    activity_record["calories"] =  str(entry[5])
                    activity_record["steps"] = str(entry[9])

                    coordinatesRAW = str(entry[11]).split(";")
                    activity_record["coordinates"] = MifitUtils.getCoordinateByBulkArray(coordinatesRAW)
                    activity_records.append(activity_record)

                    if self.gps:
                        for c in activity_record["coordinates"]:
                            self.kml_struct.add_placemark('Location1','Description1',c.split(" ")[0],c.split(" ")[1],0)

                except Exception as e:
                    logging.warning(entry)

            
            results = database.execute_query(
                    "select DEVICE_ID, DEVICE_ADDRESS, DEVICE_BIND_STATUS, DEVICE_BIND_TIME, DEVICE_SYNC_DATA_TIME, DEVICE_SYNC_DATA_TIME_HR, AUTHKEY, SN, FIRMWARE_VERSION, DEVICE_SOURCE, HARDWARE_VERSION, PRODUCT_VERSION, USER_ID from DEVICE")
            
            devices = []
            for entry in results:
                device_record = {}
                try:
                    device_record["id"] = str(entry[0])
                    device_record["address"] = str(entry[1])
                    device_record["bindStatus"] = str(entry[2])
                    device_record["bindTime"] = int(entry[3]/1000)
                    device_record["syncDataTime"] = int(entry[4]/1000)
                    device_record["syncDataTimeHR"] = int(entry[5]/1000)
                    device_record["authkey"] = str(entry[6])
                    device_record["sn"] = str(entry[7])
                    device_record["firmwareVersion"] = str(entry[8])
                    device_record["type"] = str(entry[9])
                    device_record["hardwareVersion"] = str(entry[10])
                    device_record["productVersion"] = str(entry[11])
                    device_record["userId"] = str(entry[12])
                    devices.append(device_record)
                except:
                    pass


            results = database.execute_query(
                    "select USER_ID, NAME, AVATAR_URL, HEIGHT, WEIGHT, LAST_LOGIN_TIME from USER_INFOS")
            
            users_details = []
            for entry in results:
                user_details = {}
                try:
                    user_details["id"] = str(entry[0])
                    user_details["name"] = str(entry[1])
                    user_details["avatar"] = str(entry[2])
                    user_details["height"] = str(entry[3])
                    user_details["weight"] = str(entry[4])
                    user_details["lastLoginTime"] = int(entry[5])
                    users_details.append(user_details)
                except:
                    pass
        
            results = database.execute_query(
                    "select GOAL_STEPS_COUNT, WEAR_HAND, WEATHER_SETTING from CONFIG")
            
            config_details = []
            for entry in results:
                config_detail = {}
                try:
                    config_detail["goalSteps"] = str(entry[0])
                    config_detail["wearHand"] = str(entry[1])
                    config_detail["weatherSetting"] = json.loads(entry[2])
                    config_details.append(config_detail)
                except:
                    pass
            
            return {"hr": hr_records, "alarm": alarm_records, "sleep": sleep_records, "steps": step_records, "workouts": activity_records, "devices": devices, "userDetails": users_details, "configDetails": config_details }
        except:
            pass

    def __analyze_stress(self, database_path):
        
        logging.info("Parsing Stress Data")
        
        stress_records = []

        try:
            database = Database(database_path)
            results = database.execute_query(
                "select data from AllDayStress;")

            for entry in results:
                try:
                    records = json.loads(entry[0])
                    if records:
                        for record in records:
                            if(not Utils.is_timestamp_between_timestamps((int(record.get("time"))/1000), self.start_date, self.end_date)):
                                continue
                            stress_record = {}
                            stress_record["time"] = int(record.get("time"))/1000
                            stress_record["value"] = str(record.get("value"))
                            stress_records.append(stress_record)
                except:
                    pass

        except Exception as e:
            pass
            # logging.warning(e)
        
        return {"allDayStress": stress_records}

        
    def __analyze_spo(self, database_path):
        
        logging.info("Parsing SPO Data")
        
        spo_records = []

        try:
            database = Database(database_path)
            results = database.execute_query(
                "select utcTimestamp, spo2, deviceId from click_measured_spo2")

            for entry in results:
                try:
                    if(not Utils.is_timestamp_between_timestamps(int(entry[0])/1000, self.start_date, self.end_date)):
                        continue
                    spo_record = {}
                    spo_record["time"] = int(entry[0]/1000)
                    spo_record["value"] = int(entry[1])
                    spo_record["device"] = str(entry[2])
                    spo_records.append(spo_record)
                except:
                    pass

        except Exception as e:
            pass
            # logging.warning(e)
        
        return {"spo": spo_records}
        

    def __analyze_female(self, database_path):
        
        logging.info("Parsing Female Health Data")
        
        menstruation_history_records = []
        menstruation_records = []
        symptoms_records = []

        try:
            database = Database(database_path)
            results = database.execute_query(
                "select menstrualPeriod, menstrualEndTime, userId from MenstruationHistory;")

            for entry in results:
                try:
                    menstruation_history_record = {}
                    menstruation_history_record["start"] = int(entry[0])
                    menstruation_history_record["end"] = int(entry[1])
                    menstruation_history_record["userId"] = int(entry[2])
                    menstruation_history_records.append(menstruation_history_record)
                except Exception as e:
                    pass

            
            results = database.execute_query(
                "select updateTime, date from MenstruationRecord;")

            for entry in results:
                try:
                    menstruation_record = {}
                    menstruation_record["updateTime"] = int(entry[0])
                    menstruation_record["date"] = int(entry[1])
                    menstruation_records.append(menstruation_record)
                except Exception as e:
                    pass

            
            results = database.execute_query(
                "select date, type from Symptom;")

            for entry in results:
                try:
                    symptoms_record = {}
                    symptoms_record["date"] = int(entry[0])
                    symptoms_record["type"] = str(entry[1])
                    symptoms_records.append(symptoms_record)
                except Exception as e:
                    pass

        except Exception as e:
            pass
        
        return { "history": menstruation_history_records, "records": menstruation_records, "symptoms": symptoms_records}
        
    def __analyze_sdk(self, xml_path):
        values = Utils.xml_attribute_finder(xml_path)
        user_info = {}
        users = []
        for key, value in values.items():
            user_info = {}
            try:
                if key == "ti":
                    dump = json.loads(value)
                    user_info["provider"] = str(dump.get("provider"))
                    user_info["registDate"] = int(dump.get("regist_info").get("regist_date"))
                    user_info["countryCode"] = str(dump.get("regist_info").get("country_code"))
                    user_info["appToken"] = str(dump.get("token_info").get("app_token"))
                    user_info["loginToken"] = str(dump.get("token_info").get("login_token"))
                    user_info["idToken"] = str(dump.get("token_info").get("user_id"))
                    user_info["email"] = str(dump.get("thirdparty_info").get("email"))
                    user_info["nickname"] = str(dump.get("thirdparty_info").get("nickname"))
                    user_info["thirdId"] = str(dump.get("thirdparty_info").get("third_id"))
                    users.append(user_info)
            except Exception as e:
                logging.warning(e)
                
            
        return {"userInfo": users}
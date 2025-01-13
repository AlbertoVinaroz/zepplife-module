import json
import logging
import os
import sys

from package.database import Database
from gps import Kml
from ZL_std import Standalone
from utils import BlackBoardUtils, MifitUtils, Utils
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.ingest import DataSourceIngestModule, IngestModule
from org.sleuthkit.datamodel import BlackboardArtifact, BlackboardAttribute



class MifitIngestModule(DataSourceIngestModule):
    def __init__(self, settings):
        # Set logging path to autopsy log
        Utils.setup_custom_logger(os.path.join(
            Case.getCurrentCase().getLogDirectoryPath(), "autopsy.log.0"))
        self.artifacts = {
            'userDetails': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_USER_DETAILS", "MIFIT_USER_DETAILS", BlackboardArtifact.Category.DATA_ARTIFACT),
            'configDetails': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_CONFIG_DETAILS", "MIFIT_CONFIG_DETAILS", BlackboardArtifact.Category.DATA_ARTIFACT),
            'heartRate': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_HR", "MIFIT_HR", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_HR", "MIFIT_HR", "Heart Rate Records"),
            'alarm': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_ALARM", "MIFIT_ALARM", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_ALARM", "MIFIT_ALARM", "Alarms"),
            'steps': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_STEPS", "MIFIT_STEPS", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_STEPS", "MIFIT_STEPS", "Steps"),
            'sleep': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_SLEEP", "MIFIT_SLEEP", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_SLEEP", "MIFIT_SLEEP", "Sleep"),
            'workout': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_WORKOUT", "MIFIT_WORKOUT", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_WORKOUT", "MIFIT_WORKOUT", "Workouts"),
            #'userInfo': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_USER", "MIFIT_USER", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_USER", "MIFIT_USER", "User Info"),
            'stress': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_STRESS", "MIFIT_STRESS", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_STRESS", "MIFIT_STRESS", "Stress"),
            'spo': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_SPO", "MIFIT_SPO", BlackboardArtifact.Category.DATA_ARTIFACT)
            #BlackBoardUtils.create_artifact_type("MIFIT_SPO", "MIFIT_SPO", "Spo2"),
            #'fhHistory': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_FH_HISTORY", "MIFIT_FH_HISTORY", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_FH_HISTORY", "MIFIT_FH_HISTORY", "Female Health - History"),
            #'fhRecords': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_FH_RECORDS", "MIFIT_FH_RECORDS", BlackboardArtifact.Category.DATA_ARTIFACT),
            #BlackBoardUtils.create_artifact_type("MIFIT_FH_RECORDS", "MIFIT_FH_RECORDS", "Female Health - Records"),
            #'fhSymptoms': Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType("MIFIT_FH_SYMPTOMS", "MIFIT_FH_SYMPTOMS", BlackboardArtifact.Category.DATA_ARTIFACT) }
            #BlackBoardUtils.create_artifact_type("MIFIT_FH_SYMPTOMS", "MIFIT_FH_SYMPTOMS", "Female Health - Symptoms")        }
        }


        self.attributes = {
            'goalSteps': BlackBoardUtils.create_attribute_type('MIFIT_GOAL_STEPS', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Goal Steps"),
            'wearHand': BlackBoardUtils.create_attribute_type('MIFIT_WEAR_HAND', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Wear Hand"),
            'city': BlackBoardUtils.create_attribute_type('MIFIT_CITY', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "City"),
            'locationKey': BlackBoardUtils.create_attribute_type('MIFIT_LOCATION_KEY', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Location Key"),
            'affiliation': BlackBoardUtils.create_attribute_type('MIFIT_AFFILIATION', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Affiliation"),
            'id': BlackBoardUtils.create_attribute_type('MIFIT_ID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Id"),
            'name': BlackBoardUtils.create_attribute_type('MIFIT_NAME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Name"),
            'avatar': BlackBoardUtils.create_attribute_type('MIFIT_AVATAR', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Avatar"),
            'height': BlackBoardUtils.create_attribute_type('MIFIT_HEIGHT', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Height"),
            'weight': BlackBoardUtils.create_attribute_type('MIFIT_WEIGHT', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Weight"),
            'lastLoginTime': BlackBoardUtils.create_attribute_type('MIFIT_LAST_LOGIN', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Last login"),
            'heartRate': BlackBoardUtils.create_attribute_type('MIFIT_HR', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Heart Rate"),
            'enabled': BlackBoardUtils.create_attribute_type('MIFIT_ENABLED', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Enabled"),
            'start': BlackBoardUtils.create_attribute_type('MIFIT_START', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Start"),
            'stop': BlackBoardUtils.create_attribute_type('MIFIT_STOP', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Stop"),
            'mode': BlackBoardUtils.create_attribute_type('MIFIT_MODE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Mode"),
            'distance': BlackBoardUtils.create_attribute_type('MIFIT_DISTANCE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Distance"),
            'calories': BlackBoardUtils.create_attribute_type('MIFIT_CALORIES', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Calories"),
            'steps': BlackBoardUtils.create_attribute_type('MIFIT_STEPS', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Steps"),
            'type': BlackBoardUtils.create_attribute_type('MIFIT_TYPE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Type"),
            'datestr': BlackBoardUtils.create_attribute_type('MIFIT_DATESTR', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Date"),
            'cadence': BlackBoardUtils.create_attribute_type('MIFIT_CADENCE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Cadence"),
            'startTime': BlackBoardUtils.create_attribute_type('MIFIT_STARTTIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Start Time"),
            'endTime': BlackBoardUtils.create_attribute_type('MIFIT_ENDTIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "End Time"),
            'from': BlackBoardUtils.create_attribute_type('MIFIT_FROM', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "From"),
            'to': BlackBoardUtils.create_attribute_type('MIFIT_TO', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "To"),
            'provider': BlackBoardUtils.create_attribute_type('MIFIT_PROVIDER', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Provider"),
            'registDate': BlackBoardUtils.create_attribute_type('MIFIT_REGIST', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Regist Date"),
            'appToken': BlackBoardUtils.create_attribute_type('MIFIT_APPTOKEN', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "App Token"),
            'loginToken': BlackBoardUtils.create_attribute_type('MIFIT_LOGINTOKEN', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Login Token"),
            'idToken': BlackBoardUtils.create_attribute_type('MIFIT_IDTOKEN', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Token Id"),
            'thirdId': BlackBoardUtils.create_attribute_type('MIFIT_THIRDID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Third Party Id"),
            'stress': BlackBoardUtils.create_attribute_type('MIFIT_STRESS', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Stress Value"),
            'spo': BlackBoardUtils.create_attribute_type('MIFIT_SPO', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Spo Value"),
            'bindStatus': BlackBoardUtils.create_attribute_type('MIFIT_BIND_STATUS', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Bind Status"),
            'bindTime': BlackBoardUtils.create_attribute_type('MIFIT_BIND_TIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Bind Time"),
            'syncDataTime': BlackBoardUtils.create_attribute_type('MIFIT_SYNC_DATATIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Sync Data Time"),
            'syncDataTimeHR': BlackBoardUtils.create_attribute_type('MIFIT_SYNC_DATATIME_HR', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Sync Data Time HR"),
            'authkey': BlackBoardUtils.create_attribute_type('MIFIT_AUTH_KEY', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Auth Key"),
            'sn': BlackBoardUtils.create_attribute_type('MIFIT_SN', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "S/N"),
            'firmwareVersion': BlackBoardUtils.create_attribute_type('MIFIT_FIRMWARE_VERSION', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Firmware Version"),
            'type': BlackBoardUtils.create_attribute_type('MIFIT_TYPE', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Type"),
            'hardwareVersion': BlackBoardUtils.create_attribute_type('MIFIT_HARDWARE_VERSION', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Hardware Version"),
            'productVersion': BlackBoardUtils.create_attribute_type('MIFIT_PRODUCT_VERSION', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "Product Version"),
            'userId': BlackBoardUtils.create_attribute_type('MIFIT_USERID', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING, "User ID"),
            'updateTime': BlackBoardUtils.create_attribute_type('MIFIT_UPDATETIME', BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME, "Update Time")        }
        
        # Context of the ingest
        self.context = None

        # Module Settings choosed in ingest settings
        self.settings = settings

        # Filemanager for this case
        self.fileManager = Case.getCurrentCase().getServices().getFileManager()
    
    def get_info(self, attr=""):
        try:
            if self.report.get("report").get(attr): 
                return self.report.get("report").get(attr)
            else:
                return {}
        except Exception as e:
            logging.warning(str(e))
            return {}

    def startUp(self, context):
        # Set the environment context
        self.context = context

    def process(self, dataSource, progressBar):
        # Set progressbar to an scale of 100%
        self.progressBar = progressBar
        progressBar.switchToDeterminate(100)

        self.start_date = self.settings.getSetting('startDate')
        self.end_date = self.settings.getSetting('endDate')
        self.options = json.loads(self.settings.getSetting('options')) if self.settings.getSetting('options') else ["Index GPS Coordinates"]
        self.is_gps = "Index GPS Coordinates" in self.options

        logging.info("Start Date {}".format(self.settings.getSetting('startDate')))
        logging.info("End Date {}".format(self.settings.getSetting('endDate')))
        logging.info("Options {}".format(self.settings.getSetting('options')))
        self.temp_module_path = os.path.join(Case.getCurrentCase().getModulesOutputDirAbsPath(), "Mifit")
        Utils.check_and_generate_folder(self.temp_module_path)

        file = self.fileManager.findFiles(dataSource, "%origin%")[0]
        standalone = Standalone(os.path.dirname(os.path.dirname(file.getLocalPath())), "report.json", self.start_date, self.end_date, True)

        self.report = standalone.analyse()
        file_handler = open(os.path.join(self.temp_module_path, "report.json"), "w")
        file_handler.write(json.dumps(self.report))
        file_handler.close()

        for entry in self.get_info("origin").get("devices"):
            try:
                artifact = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_BLUETOOTH_ADAPTER)
                attributes = [
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DEVICE_ID, file.getLocalPath(), entry.get("id")),
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_MAC_ADDRESS, file.getLocalPath(), entry.get("address")),
                    BlackboardAttribute(self.attributes.get('bindStatus'), file.getLocalPath(), entry.get("bindStatus")),
                    BlackboardAttribute(self.attributes.get('bindTime'), file.getLocalPath(), entry.get("bindTime")),
                    BlackboardAttribute(self.attributes.get('syncDataTime'), file.getLocalPath(), entry.get("syncDataTime")),
                    BlackboardAttribute(self.attributes.get('syncDataTimeHR'), file.getLocalPath(), entry.get("syncDataTimeHR")),
                    BlackboardAttribute(self.attributes.get('authkey'), file.getLocalPath(), entry.get("authkey")),
                    BlackboardAttribute(self.attributes.get('sn'), file.getLocalPath(), entry.get("sn")),
                    BlackboardAttribute(self.attributes.get('firmwareVersion'), file.getLocalPath(), entry.get("firmwareVersion")),
                    BlackboardAttribute(self.attributes.get('type'), file.getLocalPath(), entry.get("type")),
                    BlackboardAttribute(self.attributes.get('hardwareVersion'), file.getLocalPath(), entry.get("hardwareVersion")),
                    BlackboardAttribute(self.attributes.get('productVersion'), file.getLocalPath(), entry.get("productVersion")),
                    BlackboardAttribute(self.attributes.get('userId'), file.getLocalPath(), entry.get("userId"))
                    ]
                
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('steps'), attributes)
                if self.is_gps:
                    for coordinate in entry.get("coordinates"):
                        try:
                            BlackBoardUtils.add_tracking_point(file, entry.get("start"), coordinate.split(" ")[0], coordinate.split(" ")[1], source=file.getLocalPath())
                        except:
                            pass
            except Exception as e:
                logging.warning(str(e))


        for entry in self.get_info("origin").get("hr"):
            try:
                artifact = file.newArtifact(self.artifacts.get('heartRate').getTypeID())
                attributes = [
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DATETIME, file.getLocalPath(), entry.get("time")),
                    BlackboardAttribute(self.attributes.get('heartRate'), file.getLocalPath(), entry.get("value")),
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DEVICE_ID, file.getLocalPath(), entry.get("device"))
                ]
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('heartRate'), attributes)
            except Exception as e:
                logging.warning(str(e))

        
        for entry in self.get_info("spo").get("spo"):
            try:
                artifact = file.newArtifact(self.artifacts.get('spo').getTypeID())
                attributes = [
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DATETIME, file.getLocalPath(), entry.get("time")),
                    BlackboardAttribute(self.attributes.get('spo'), file.getLocalPath(), str(entry.get("value"))),
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DEVICE_ID, file.getLocalPath(), entry.get("device"))
                ]
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('spo'), attributes)
            except Exception as e:
                logging.warning(str(e))

        
        for entry in self.get_info("origin").get("sleep"):
            try:
                artifact = file.newArtifact(self.artifacts.get('sleep').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('datestr'), file.getLocalPath(), entry.get("date")),
                    BlackboardAttribute(self.attributes.get('from'), file.getLocalPath(), entry.get("from")),
                    BlackboardAttribute(self.attributes.get('to'), file.getLocalPath(), entry.get("to")),
                    BlackboardAttribute(self.attributes.get('mode'), file.getLocalPath(), entry.get("mode"))
                    ]
                
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('sleep'), attributes)
            except Exception as e:
                logging.warning(str(e))

        for entry in self.get_info("origin").get("alarm"):
            try:
                artifact = file.newArtifact(self.artifacts.get('alarm').getTypeID())
                attributes = [
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DATETIME, file.getLocalPath(), entry.get("time")/1000),
                    BlackboardAttribute(self.attributes.get('enabled'), file.getLocalPath(), entry.get("enabled"))
                ]
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('alarm'), attributes)
            except Exception as e:
                logging.warning(str(e))
        
        for entry in self.get_info("origin").get("steps"):
            try:
                artifact = file.newArtifact(self.artifacts.get('steps').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('datestr'), file.getLocalPath(), entry.get("date")),
                    BlackboardAttribute(self.attributes.get('from'), file.getLocalPath(), entry.get("from")),
                    BlackboardAttribute(self.attributes.get('to'), file.getLocalPath(), entry.get("to")),
                    BlackboardAttribute(self.attributes.get('mode'), file.getLocalPath(), entry.get("mode")),
                    BlackboardAttribute(self.attributes.get('distance'), file.getLocalPath(), entry.get("distance")),
                    BlackboardAttribute(self.attributes.get('calories'), file.getLocalPath(), entry.get("calories")),
                    BlackboardAttribute(self.attributes.get('steps'), file.getLocalPath(), entry.get("steps"))
                    ]
                
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('steps'), attributes)
            except Exception as e:
                logging.warning(str(e))
        
        for entry in self.get_info("origin").get("userDetails"):
            try:
                artifact = file.newArtifact(self.artifacts.get('userDetails').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('id'), file.getLocalPath(), entry.get("id")),
                    BlackboardAttribute(self.attributes.get('name'), file.getLocalPath(), entry.get("name")),
                    BlackboardAttribute(self.attributes.get('avatar'), file.getLocalPath(), entry.get("avatar")),
                    BlackboardAttribute(self.attributes.get('height'), file.getLocalPath(), entry.get("height")),
                    BlackboardAttribute(self.attributes.get('weight'), file.getLocalPath(), entry.get("weight")),
                    BlackboardAttribute(self.attributes.get('lastLoginTime'), file.getLocalPath(), entry.get("lastLoginTime"))
                    ]
                
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('userDetails'), attributes)
            except Exception as e:
                logging.warning(str(e))
        
        for entry in self.get_info("origin").get("configDetails"):
            try:
                artifact = file.newArtifact(self.artifacts.get('configDetails').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('goalSteps'), file.getLocalPath(), entry.get("goalSteps")),
                    BlackboardAttribute(self.attributes.get('wearHand'), file.getLocalPath(), entry.get("wearHand")),
                    BlackboardAttribute(self.attributes.get('city'), file.getLocalPath(), entry.get("weatherSetting").get("city")),
                    BlackboardAttribute(self.attributes.get('locationKey'), file.getLocalPath(), entry.get("weatherSetting").get("locationKey")),
                    BlackboardAttribute(self.attributes.get('affiliation'), file.getLocalPath(), entry.get("weatherSetting").get("affiliation"))
                    ]
                
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('configDetails'), attributes)
            except Exception as e:
                logging.warning(str(e))

        for entry in self.get_info("origin").get("workouts"):
            try:
                artifact = file.newArtifact(self.artifacts.get('steps').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('mode'), file.getLocalPath(), entry.get("type")),
                    BlackboardAttribute(self.attributes.get('start'), file.getLocalPath(), entry.get("start")),
                    BlackboardAttribute(self.attributes.get('stop'), file.getLocalPath(), entry.get("end")),
                    BlackboardAttribute(self.attributes.get('distance'), file.getLocalPath(), entry.get("distance")),
                    BlackboardAttribute(self.attributes.get('calories'), file.getLocalPath(), entry.get("calories")),
                    BlackboardAttribute(self.attributes.get('steps'), file.getLocalPath(), entry.get("steps"))
                    ]
                
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('workout'), attributes)
                if self.is_gps:
                    for coordinate in entry.get("coordinates"):
                        try:
                            BlackBoardUtils.add_tracking_point(file, entry.get("start"), coordinate.split(" ")[0], coordinate.split(" ")[1], source=file.getLocalPath())
                        except:
                            pass
            except Exception as e:
                logging.warning(str(e))
        
        
        
        for entry in self.get_info("stress").get("allDayStress"):
            try:
                artifact = file.newArtifact(self.artifacts.get('stress').getTypeID())
                attributes = [
                    BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DATETIME, file.getLocalPath(), entry.get("time")),
                    BlackboardAttribute(self.attributes.get('stress'), file.getLocalPath(), entry.get("value")),
                ]
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('stress'), attributes)
            except Exception as e:
                logging.warning(str(e))

        # for entry in self.get_info("users").get("userInfo"):
        #     try:
        #         artifact = file.newArtifact(self.artifacts.get('userInfo'))
        #         attributes = [
        #             BlackboardAttribute(self.attributes.get('provider'), file.getLocalPath(), entry.get("provider")),
        #             BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_COUNTRY, file.getLocalPath(), entry.get("provider")),
        #             BlackboardAttribute(self.attributes.get('registDate'), file.getLocalPath(), entry.get("registDate")/1000),
        #             BlackboardAttribute(self.attributes.get('appToken'), file.getLocalPath(), entry.get("appToken")),
        #             BlackboardAttribute(self.attributes.get('loginToken'), file.getLocalPath(), entry.get("loginToken")),
        #             BlackboardAttribute(self.attributes.get('idToken'), file.getLocalPath(), entry.get("idToken")),
        #             BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_EMAIL, file.getLocalPath(), entry.get("email")),
        #             BlackboardAttribute(BlackboardAttribute.ATTRIBUTE_TYPE.TSK_NAME_PERSON, file.getLocalPath(), entry.get("nickname")),
        #             BlackboardAttribute(self.attributes.get('thirdId'), file.getLocalPath(), entry.get("thirdId"))
        #         ]
        #         BlackBoardUtils.index_artifact(artifact, self.artifacts.get('userInfo'), attributes)
        #     except:
        #             pass
        
"""        for entry in self.get_info("female").get("history"):
            try:
                artifact = file.newArtifact(self.artifacts.get('fhHistory').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('startTime'), file.getLocalPath(), entry.get("start")/1000),
                    BlackboardAttribute(self.attributes.get('endTime'), file.getLocalPath(), entry.get("end")/1000)
                ]
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('fhHistory'), attributes)
            except Exception as e:
                print(e)
                pass

        for entry in self.get_info("female").get("records"):
            try:
                artifact = file.newArtifact(self.artifacts.get('fhRecords').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('updateTime'), file.getLocalPath(), entry.get("updateTime")/1000),
                    BlackboardAttribute(self.attributes.get('startTime'), file.getLocalPath(), entry.get("startTime")/1000)
                ]
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('fhHistory'), attributes)
            except Exception as e:
                print(e)
                pass
        
        for entry in self.get_info("female").get("symptoms"):
            try:
                artifact = file.newArtifact(self.artifacts.get('fhSymptoms').getTypeID())
                attributes = [
                    BlackboardAttribute(self.attributes.get('startTime'), file.getLocalPath(), entry.get("date")/1000),
                    BlackboardAttribute(self.attributes.get('type'), file.getLocalPath(), entry.get("type"))
                ]
                BlackBoardUtils.index_artifact(artifact, self.artifacts.get('fhHistory'), attributes)
            except Exception as e:
                print(e)
                pass """

class ProgressJob:
    def __init__(self, progressBar, jobs, maxValue=100):
        if jobs < 1:
            jobs = 1
        if maxValue < 1:
            maxValue = 1

        self.maxValue = maxValue
        self.atualPercent = 0
        self.increment = int(100 / (jobs + 1))
        self.progressBar = progressBar

    def next_job(self, message):
        self.atualPercent += self.increment

        if self.atualPercent > self.maxValue:
            self.atualPercent = self.maxValue

        self.progressBar.progress(message, self.atualPercent)

    def change_text(self, message):
        self.progressBar.progress(message)

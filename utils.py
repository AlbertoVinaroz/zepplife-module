from distutils.dir_util import mkpath
from distutils.errors import DistutilsFileError
import json
import logging
import os
import shutil
import datetime
import sys
import time
import xml.etree.ElementTree as ET
sys.path.append(os.path.dirname(__file__))


if not (sys.executable and "python" in sys.executable.lower()):
    from java.awt import Component
    from java.util import UUID
    from javax.swing import BoxLayout, JCheckBox, JPanel, JRadioButton, JTextArea, JTextField
    from javax.swing.border import EmptyBorder
    from org.sleuthkit.autopsy.casemodule import Case
    from org.sleuthkit.autopsy.casemodule.services import Blackboard
    from org.sleuthkit.autopsy.coreutils import Version
    from org.sleuthkit.autopsy.geolocation.datamodel import BookmarkWaypoint
    from org.sleuthkit.autopsy.ingest import IngestMessage, IngestServices, ModuleDataEvent
    from org.sleuthkit.datamodel import BlackboardArtifact, BlackboardAttribute, CommunicationsManager


class Utils:

    @staticmethod
    def setup_custom_logger(logfile="module.log"):
        formatting = '[%(asctime)s] %(levelname)s [%(module)s] - %(message)s'

        # FILE HANDLER
        logging.basicConfig(level=logging.DEBUG,
                            format=formatting, filemode='a', filename=logfile)

        # STREAM HANDLER
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(formatting))
        logging.getLogger().addHandler(console)
    
    @staticmethod
    def setup_case():
        env_path = os.path.join('.env')
        if not os.path.exists(env_path):
            return None

        handler = open(env_path, 'r')
        contents = handler.read()
        handler.close()

        for line in contents.splitlines():
            items = line.split('=')
            if not len(items) > 1:
                continue

            os.environ[items[0].strip()] = '='.join(items[1:]).strip()

    @staticmethod
    def list_files(source, pattern ="", exclude=[]):
        matches = []
        for root, dirnames, filenames in os.walk(source):
            for filename in filenames:
                if (pattern in filename) and not any(ele in filename for ele in exclude):
                    matches.append(os.path.join(root, filename))
        return matches
    
    @staticmethod
    def get_base_path_folder():
        return os.path.dirname((os.path.dirname(__file__)))

    @staticmethod
    def check_and_generate_folder(path):
        if not os.path.exists(path):
            return os.makedirs(path)

        return True

    @staticmethod
    def remove_folder(folder):
        shutil.rmtree(folder, ignore_errors=True)

    @staticmethod
    def read_json(path):
        f = open(path, "r")
        contents = json.loads(f.read())
        f.close()
        return contents
    
    @staticmethod
    def write_json(path, contents):
        f = open(path, "w")
        f.write(json.dumps(contents, indent=2))
        f.close()

    @staticmethod
    def verify_header_signature(file, header_type, offset, stream=None):
        header = b""
        if stream:
            header = stream.read(32)
        else:
            try:
                with open(file, "rb") as f:
                    header = f.read(32)
            except Exception as e:
                logging.warning(str(e))

        query = header.find(header_type)  # query includes position of header

        return query == offset

    @staticmethod
    def minutes_to_time(minutes):
        return "{:02d}:{:02d}".format((minutes // 60) % 24, minutes % 60)

    @staticmethod
    def timestamp_to_time(timestamp):
        return str(datetime.datetime.fromtimestamp(timestamp))

    @staticmethod
    def date_to_timestamp(date, date_format, default=None, print_error=True):
        try:
            timestamp = int(time.mktime(datetime.datetime.strptime(date, date_format).timetuple()))
            return timestamp
        except Exception as e:
            if print_error:
                logging.warning("Invalid date {} ({}) to be convert to timestamp. Using {} by default.".format(date, date_format, default))
            return default
    
    @staticmethod
    def is_timestamp_between_timestamps(timestamp, lower_limit=0, upper_limit=9999999999):
        if not timestamp:
            return True
        else:
            return int(lower_limit) <= int(timestamp) <= int(upper_limit)
    
    @staticmethod
    def get_current_timestamp():
        return int(time.time())

    @staticmethod
    def get_current_date(date_format):
        return datetime.datetime.today().strftime(date_format)

    @staticmethod
    def is_valid_date(date, date_format="%Y/%m/%d"):
        try:
            datetime.datetime.strptime(date, date_format)
            return True
        except Exception:
            return False
    
    @staticmethod
    def xml_attribute_finder(xml_path, attrib_values = None):
        listing = {}
        if not os.path.exists(xml_path):
            return None
            
        root = ET.parse(xml_path).getroot()
        for child in root:
            if not attrib_values or child.attrib.get("name") in attrib_values:
                if child.attrib.get("value"):
                    value= child.attrib.get("value")
                else:
                    value = child.text

                try:
                    listing[child.attrib.get("name")] = str(value)
                except:
                    listing[child.attrib.get("name")] = str(value.encode('utf-8','ignore'))

        return listing

    @staticmethod
    def get_autopsy_version():
        item = {"major": 0, "minor": 0, "patch": 0}

        version = Version.getVersion().split('.')
        
        try:
            if len(version) >= 1:
                item["major"] = int(version[0])
            
            if len(version) >= 2:
                item["minor"] = int(version[1])

            if len(version) >= 3:
                item["patch"] = int(version[2])
        except:
            pass
        
        return item

    @staticmethod
    def copy_tree(src, dst, preserve_mode=1, preserve_times=1, preserve_symlinks=0, update=0, verbose=1, dry_run=0):
        #OVERRIDE FROM DSTUTILS METHOD
        from distutils.file_util import copy_file

        if not dry_run and not os.path.isdir(src):
            raise DistutilsFileError(
                "cannot copy tree '%s': not a directory" % src)
        try:
            names = os.listdir(src)
        except OSError as e:
            if dry_run:
                names = []
            else:
                raise DistutilsFileError(
                    "error listing files in '%s': %s" % (src, e.strerror))

        if not dry_run:
            mkpath(dst, verbose=verbose)

        outputs = []

        for n in names:
            src_name = os.path.join(src, n)
            dst_name = os.path.join(dst, n)

            if n.startswith('.nfs'):
                continue

            if preserve_symlinks and os.path.islink(src_name):
                link_dest = os.readlink(src_name)
                if verbose >= 1:
                    logging.info("linking %s -> %s", dst_name, link_dest)
                if not dry_run:
                    os.symlink(link_dest, dst_name)
                outputs.append(dst_name)

            elif os.path.isdir(src_name):
                outputs.extend(
                    Utils.copy_tree(src_name, dst_name, preserve_mode,
                            preserve_times, preserve_symlinks, update,
                            verbose=verbose, dry_run=dry_run))
            else:
                try:
                    copy_file(src_name, dst_name, preserve_mode,
                            preserve_times, update, verbose=verbose,
                            dry_run=dry_run)
                    outputs.append(dst_name)
                except:
                    pass

        return outputs


class BlackBoardUtils:

    @staticmethod
    def post_message(msg):
        IngestServices.getInstance().postMessage(
            IngestMessage.createMessage(IngestMessage.MessageType.DATA, "Mifit", msg))

    @staticmethod
    def create_attribute_type(att_name, type, att_desc):
        try:
            Case.getCurrentCase().getSleuthkitCase(
            ).addArtifactAttributeType(att_name, type, att_desc)
        except:
            logging.warning("Error creating attribute type: " + att_desc)
            pass
        return Case.getCurrentCase().getSleuthkitCase().getAttributeType(att_name)

    @staticmethod
    def create_artifact_type(base_name, art_name, art_desc):
        try:
            artifactType = Case.getCurrentCase().getSleuthkitCase().getArtifactType(art_name)
            if (artifactType == None):
                Case.getCurrentCase().getSleuthkitCase().addBlackboardArtifactType(art_name, base_name + ": " + art_desc)
            #at = Case.getCurrentCase().getSleuthkitCase().addBlackboardArtifactType(art_name, base_name + ": " + art_desc)
            #logging.warning(Case.getCurrentCase().getSleuthkitCase().getBlackboard().getOrAddArtifactType(
            #art_name, base_name + ": " + art_desc, BlackboardArtifact.Category.DATA_ARTIFACT))
        except:
            logging.warning("Error creating artifact type: " + art_desc)
            pass
        
        return Case.getCurrentCase().getSleuthkitCase().getArtifactType(art_name)#{ 'artifactType': artifactType, 'typeId': artifactType.getTypeID()}

    @staticmethod
    def get_artifacts_list():
        listing = []
        try:
            listing = Case.getCurrentCase().getSleuthkitCase().getArtifactTypesInUse()
        except:
            logging.warning("Error getting artifacts list")

        return listing

    @staticmethod
    def index_artifact(artifact, artifact_type, attributes=[]):
        try:
            artifact.addAttributes(attributes)
            Case.getCurrentCase().getServices().getBlackboard().indexArtifact(artifact)
        except:
            logging.warning("Error indexing artifact type: " + artifact_type)
        #IngestServices.getInstance().fireModuleDataEvent(ModuleDataEvent("Mifit", artifact_type, None))

    @staticmethod
    def add_relationship(node1, node2, art, relationship_type, timestamp):
        Case.getCurrentCase().getSleuthkitCase().getCommunicationsManager(
        ).addRelationships(node1, node2, art, relationship_type, timestamp)

    @staticmethod
    def add_tracking_point(file, timestamp=0, latitude=0, longitude=0, altitude=0, source="source"):

        art = file.newArtifact(
            BlackboardArtifact.ARTIFACT_TYPE.TSK_GPS_TRACKPOINT)
        art.addAttribute(BlackboardAttribute(
            BlackboardAttribute.ATTRIBUTE_TYPE.TSK_GEO_LATITUDE, source, float(latitude)))
        art.addAttribute(BlackboardAttribute(
            BlackboardAttribute.ATTRIBUTE_TYPE.TSK_GEO_LONGITUDE, source, float(longitude)))
        art.addAttribute(BlackboardAttribute(
            BlackboardAttribute.ATTRIBUTE_TYPE.TSK_GEO_ALTITUDE, source, float(altitude)))
        art.addAttribute(BlackboardAttribute(
            BlackboardAttribute.ATTRIBUTE_TYPE.TSK_DATETIME, source, timestamp))
        BookmarkWaypoint(art)
        return art

    @staticmethod
    def get_or_create_account(account_type, file, uniqueid):
        return Case.getCurrentCase().getSleuthkitCase().getCommunicationsManager().createAccountFileInstance(account_type, uniqueid, "test", file.getDataSource())

    @staticmethod
    def add_account_type(accountTypeName, displayName):
        communication_manager = Case.getCurrentCase(
        ).getSleuthkitCase().getCommunicationsManager()
        return CommunicationsManager.addAccountType(communication_manager, accountTypeName, displayName)
    
   


class SettingsUtils:

    @staticmethod
    def createPanel(scroll=False, ptop=0, pleft=0, pbottom=0, pright=0):
        panel = JPanel()
        panel.setLayout(BoxLayout(panel, BoxLayout.PAGE_AXIS))
        panel.setAlignmentX(Component.LEFT_ALIGNMENT)
        panel.setBorder(EmptyBorder(ptop, pleft, pbottom, pright))
        return panel

    @staticmethod
    def createRadioButton(name, ac, ap):
        button = JRadioButton(name, actionPerformed=ap)
        button.setActionCommand(ac)
        return button

    @staticmethod
    def createInfoLabel(text):
        textArea = JTextArea()
        textArea.setLineWrap(True)
        textArea.setWrapStyleWord(True)
        textArea.setOpaque(False)
        textArea.setEditable(False)
        textArea.setText(text)
        return textArea

    @staticmethod
    def createSeparators(count):
        lines = ""
        for i in range(count):
            lines += "<br>"

        return SettingsUtils.createInfoLabel(lines)

    @staticmethod
    def createCheckbox(label, ap, visible=False):
        checkbox = JCheckBox("{}".format(label), actionPerformed=ap)
        checkbox.setActionCommand(label)
        checkbox.setSelected(True)
        checkbox.setVisible(visible)
        checkbox.setActionCommand(label)
        return checkbox
    
    @staticmethod
    def createInputField(ap, enabled=True):
        textField = JTextField(10, focusLost=ap)
        textField.setEnabled(enabled)
        return textField


class MifitUtils:

    @staticmethod
    def mode_to_workout(mode):
        workout = {
            "53": "Stretching",
            "92": "Badminton",
            "85": "Basketball",
            "80": "Bowling",
            "97": "Box",
            "6": "Walking",
            "9": "Outdoor Cycling",
            "10": "Indoor Cycling",
            "TODO": "Outdoor Running",
            "78": "Cricket",
            "76": "Dance",
            "74": "Street dancing",
            "12": "Elliptical",
            "59": "Gymnastics",
            "49": "HIIT",
            "60": "Yoga",
            "16": "Free",
            "23": "Rowing Machine",
            "14": "Pool swimming",
            "8": "Treadmill",
            "45": "Indoor ice skating",
            "61": "Pilates",
            "21": "Jumping rope",
            "104": "Kickboxing",
            "58": "Stepper",
            "89": "Table tennis",
            "50": "Core training",
            "24": "Indoor training",
            "88": "Volleyball",
            "77": "Zumba"
        }.get(mode)
        return workout if workout else str(mode + " - Unknown")


    @staticmethod
    def mode_to_activity(mode):
        activity = {
            "1": "Slow Walking",
            "3": "Fast Walking",
            "4": "Running",
            "7": "Light Activity",
        }.get(mode)
        return activity if activity else str(mode + " - Unknown")

    @staticmethod
    def mode_to_sleep(mode):
        sleep = {
            "4": "Light Sleep",
            "5": "Deep Sleep",
            "7": "Time Awake",
            "8": "REM"
        }.get(mode)
        return sleep if sleep else str(mode + " - Unknown")
    
    @staticmethod    
    def getCoordianateByString(raw):
        try:
            c = {"lat": int(raw.split(",")[0]), "lon": int(raw.split(",")[1])}
            return c
        except:
            return [0, 0]

    @staticmethod
    def getCoordinateByBulkArray(bulk):
        previous = MifitUtils.getCoordianateByString(bulk[0])

        clean_coordinates = []

        for coordinate in bulk[1:]:
            current = {"lat": (previous.get("lat") + (MifitUtils.getCoordianateByString(coordinate).get("lat"))), "lon": (previous.get("lon") + (MifitUtils.getCoordianateByString(coordinate).get("lon")))}
            clean_coordinates.append("{} {}".format(current.get("lat")* 0.00000001 ,current.get("lon") * 0.00000001))
            previous = current
        return clean_coordinates

    

from org.sleuthkit.autopsy.ingest import GenericIngestModuleJobSettings
from org.sleuthkit.autopsy.report import GeneralReportModuleAdapter
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.autopsy.report.ReportProgressPanel import ReportStatus
from org.sleuthkit.autopsy.casemodule import Case


import sys, os
from ZL_std import Standalone

from utils import Utils

sys.path.append(os.path.dirname(__file__))
from gps import Kml
from ingest import MifitIngestModule
from settings import MifitIngestSettingsPanel, MifitReportSettingsPanel

class MifitIngestModuleFactory(IngestModuleFactoryAdapter):
    moduleName = "Mifit and Zepp Life Android App Analyzer"

    def __init__(self):
        self.settings = None
        
    #Module Settings
    def getModuleDisplayName(self):
        return self.moduleName

    def getModuleDescription(self):
        return "Mifit and Zepp Life Analyzer for Autopsy"
        
    def getModuleVersionNumber(self):
        return "1.0"
    
    #Data Source Ingest
    def isDataSourceIngestModuleFactory(self):
        return True

    def createDataSourceIngestModule(self, ingestOptions):
        return MifitIngestModule(self.settings)

    #Settings
    def getDefaultIngestJobSettings(self):
        return GenericIngestModuleJobSettings()
    
    def hasIngestJobSettingsPanel(self):
        return True

    def getIngestJobSettingsPanel(self, settings):
        if not isinstance(settings, GenericIngestModuleJobSettings):
            raise IllegalArgumentException("Expected settings argument to be instanceof GenericIngestModuleJobSettings")
        
        self.settings = settings
        return MifitIngestSettingsPanel(self.settings)


class MifitReportModule(GeneralReportModuleAdapter):
    moduleName = "Mifit and Zepp Life Android App Report"

    def __init__(self):
        self.settings = None
        # self.report = MifitReport()

    def getName(self):
        return self.moduleName

    def getDescription(self):
        return "Mifit and Zepp Life Android App Report Generator"

    def generateReport(self, settings, progressBar):

        progressBar.setIndeterminate(True)

        self.fileManager = Case.getCurrentCase().getServices().getFileManager()

        progressBar.updateStatusLabel("Searching for processed Mifit data...")

        self.reportFile = os.path.join(Case.getCurrentCase().getModulesOutputDirAbsPath(), "Mifit", "report.json")

        progressBar.updateStatusLabel("Creating report")
        
        os.environ["CASE_NAME"] = Case.getCurrentCase().getName()
        os.environ["CASE_NUMBER"] = Case.getCurrentCase().getNumber()
        os.environ["EXAMINER"] = Case.getCurrentCase().getExaminer()
        os.environ["CASE_DATE"] = Utils.get_current_timestamp()
        autopsy_version = Utils.get_autopsy_version()

        baseReportDir = settings
        
        if (autopsy_version["major"] == 4 and autopsy_version["minor"] >= 16):
            baseReportDir = settings.getReportDirectoryPath()
        
        report_path = os.path.join(Case.getCurrentCase().getModulesOutputDirAbsPath(), "Mifit")

        Utils.check_and_generate_folder(report_path)

        Utils.copy_tree(os.path.join(os.path.dirname(__file__), "report"), report_path)

        report = Utils.read_json(self.reportFile)
        report_html_path = Standalone.detach_report(report, os.path.join(report_path, "js", "report.js"))

        Case.getCurrentCase().addReport(report_html_path, "Report", "Forensics Report")
        progressBar.updateStatusLabel("Done")
        progressBar.complete(ReportStatus.COMPLETE)

    def getConfigurationPanel(self):
        self.configPanel = MifitReportSettingsPanel()
        return self.configPanel

    def getRelativeFilePath(self):
        return "\\..\\..\\ModuleOutput\\Mifit\\index.html"
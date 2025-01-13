import json
import sys
import os

from org.sleuthkit.autopsy.ingest import IngestModuleIngestJobSettingsPanel
from java.awt import Font, Color
from java.awt import Dimension
from java.awt import BorderLayout
from javax.swing import JPanel
from javax.swing import BoxLayout
from javax.swing import ButtonGroup
from javax.swing import JLabel
from javax.swing import JTextField
from collections import OrderedDict
from utils import Utils

sys.path.append(os.path.dirname(__file__))


from utils import SettingsUtils

class MifitIngestSettingsPanel(IngestModuleIngestJobSettingsPanel):
    def __init__(self, settings):
        self.local_settings = settings
        self.initComponents()

    def initComponents(self):
        self.options_checkboxes_list = []
        self.input_start_date = None
        self.input_end_date = None
        self.options_checkboxes_list = []
        self.setLayout(BoxLayout(self, BoxLayout.PAGE_AXIS))
        self.setPreferredSize(Dimension(300,0))
        
        # title 
        self.p_title = SettingsUtils.createPanel()
        self.lb_title = JLabel("Mifit/Zepp Life Android App Analyzer")
        self.lb_title.setFont(self.lb_title.getFont().deriveFont(Font.BOLD, 15))
        self.p_title.add(self.lb_title)
        self.add(self.p_title)
        # end of title

        self.p_panel = SettingsUtils.createPanel()
        self.p_panel.add(JLabel("Options available:"))
        
        #checkboxes
        options = ["Index GPS Coordinates"]

        for option in options:
            checkbox = SettingsUtils.createCheckbox(option,self.getSelectedOption, True)
            self.add(checkbox)
            self.options_checkboxes_list.append(checkbox)
            self.p_panel.add(checkbox)

        #text inputs
        self.p_panel.add(JLabel("Start Date (yyyy-mm-dd)"))
        start_field = SettingsUtils.createInputField(self.setInputSetting)
        start_field.setMaximumSize(Dimension( 400, 24 ))
        self.add(start_field)
        self.input_start_date = start_field
        self.p_panel.add(start_field)

        self.lb_invalid_start = JLabel("Invalid Start Date Format")
        self.lb_invalid_start.setForeground(Color.red)
        self.lb_invalid_start.setVisible(False)
        self.p_panel.add(self.lb_invalid_start)

        self.p_panel.add(JLabel("End Date (yyyy-mm-dd)"))
        end_field = SettingsUtils.createInputField(self.setInputSetting)
        end_field.setMaximumSize(Dimension( 400, 24 ))
        self.add(end_field)
        self.input_end_date = end_field
        self.p_panel.add(end_field)

        self.lb_invalid_end = JLabel("Invalid End Date Format")
        self.lb_invalid_end.setForeground(Color.red)
        self.lb_invalid_end.setVisible(False)
        self.p_panel.add(self.lb_invalid_end)

        self.add(self.p_panel)
    
    def getSelectedOption(self, event):
        selected_options = []
        
        for cb_option in self.options_checkboxes_list:
            if cb_option.isSelected():
                selected_options.append(cb_option.getActionCommand())
        
        self.local_settings.setSetting("options", json.dumps(selected_options))
    
    def setInputSetting(self, event):
       
        self.local_settings.setSetting("endDate", self.input_end_date.getText())
        
        if self.input_start_date.getText():
            if(Utils.is_valid_date(self.input_start_date.getText(), "%Y-%m-%d")):
                self.local_settings.setSetting("startDate", self.input_start_date.getText())
                self.lb_invalid_start.setVisible(False)
            else:
                self.local_settings.setSetting("startDate", "")
                self.lb_invalid_start.setVisible(True)
        else:
            self.local_settings.setSetting("startDate", "")
            self.lb_invalid_start.setVisible(False)
        
        if self.input_end_date.getText():
            if(Utils.is_valid_date(self.input_end_date.getText(), "%Y-%m-%d")):
                self.local_settings.setSetting("endDate", self.input_end_date.getText())
                self.lb_invalid_end.setVisible(False)
            else:
                self.local_settings.setSetting("endDate", "")
                self.lb_invalid_end.setVisible(True)

        else:
            self.local_settings.setSetting("endDate", "")
            self.lb_invalid_end.setVisible(False)
    
    def getSettings(self):
        return self.local_settings

    

class MifitReportSettingsPanel(JPanel):
    def __init__(self):
        pass
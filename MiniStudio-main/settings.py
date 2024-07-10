class Setting:
    def __init__(self):
        self.settings = {}
        docSettings = open('settings.txt', 'r')
        settings = docSettings.read()
        docSettings.close
        for row in settings.split('\n'):
            setting = row.split(': ')
            self.settings[setting[0]] = setting[1]

    def saveSettings(self):
        """
        fonction: Enregistre les paramettres qui sont self.settings dans le fichier paramettre
        """
        txtSettings = ''
        for key in self.settings.keys():
            txtSettings += str(key) + ': ' + str(self.settings[key]) + '\n'
        txtSettings = txtSettings[:-1]
        docSettings = open('settings.txt', 'w')
        docSettings.write(txtSettings)
        docSettings.close

    def changeBinds(self, newBinds: dict):
        """
        entrée: newBinds => dictionnaire
        fonction: change les touches rentré dans newBinds et les actualise dans self.settings
        """
        for bind in newBinds.keys():
            self.settings[bind] = newBinds[bind]

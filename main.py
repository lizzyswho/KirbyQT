from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QApplication, QWidget
import os, sys, sqlite3

script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
icon_path = os.path.join(script_dir, "Icon")  # Caminho da pasta de ícones

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)  # Certifique-se de que login.ui está no diretório correto

        # Conectar botão de login à função de troca de tela
        self.loginButton.clicked.connect(self.goToMenu)
        icon = QtGui.QIcon(os.path.join(icon_path, "login.png"))  # Ícone corrigido
        self.loginButton.setIcon(icon)
        self.loginButton.setIconSize(QtCore.QSize(40, 40))
        self.loginButton.setObjectName("exitButton")


    def goToMenu(self):
        menu = MenuScreen()
        widget.addWidget(menu)  # Adiciona a tela do menu ao QStackedWidget
        widget.setCurrentWidget(menu)  # Troca para a tela do menu


class MenuScreen(QDialog):
    def __init__(self):
        super(MenuScreen, self).__init__()
        loadUi("menu.ui", self)  # Certifique-se de que menu.ui está no diretório correto

        # Conectar botão de Cadastro
        icon = QtGui.QIcon(os.path.join(icon_path, "signUp.png"))  # Ícone corrigido
        self.signButton.setIcon(icon)
        self.signButton.setIconSize(QtCore.QSize(40, 40))
        self.signButton.setObjectName("signButton")

        # Conectar botão de Pesquisa
        icon = QtGui.QIcon(os.path.join(icon_path, "search.png"))  # Ícone corrigido
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QtCore.QSize(40, 40))
        self.searchButton.setObjectName("searchButton")

        # Conectar botão de Sobre
        icon = QtGui.QIcon(os.path.join(icon_path, "about.png"))  # Ícone corrigido
        self.aboutButton.setIcon(icon)
        self.aboutButton.setIconSize(QtCore.QSize(40, 40))
        self.aboutButton.setObjectName("aboutButton")

        # Conectar botão de Saída
        icon = QtGui.QIcon(os.path.join(icon_path, "exit.png"))  # Ícone corrigido
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(QtCore.QSize(40, 40))
        self.exitButton.setObjectName("exitButton")

# Configuração principal do aplicativo
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

# Criando a tela inicial (Login)
login_screen = LoginScreen()
widget.addWidget(login_screen)

# Configurar tamanho fixo da janela
widget.setFixedHeight(480)
widget.setFixedWidth(640)

widget.show()  # Exibe a primeira tela (Login)
sys.exit(app.exec())

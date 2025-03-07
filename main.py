from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os, sys

# Criar a aplicação Qt primeiro
app = QtWidgets.QApplication(sys.argv)  # Inicializa o ambiente Qt

# Criar conexão com o banco de dados

db = QSqlDatabase.addDatabase("QSQLITE")  # Corrigindo o driver

db.setDatabaseName("shopData.db")  # Nome do banco de dados

if not db.open():
    print("Erro ao conectar ao banco de dados:", db.lastError().text())

script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
icon_path = os.path.join(script_dir, "Icon")  # Caminho da pasta de ícones

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)  

        # Conectar botão de login à função de troca de tela
        self.loginButton.clicked.connect(self.goToMenu)
        icon = QtGui.QIcon(os.path.join(icon_path, "login.png"))  
        self.loginButton.setIcon(icon)
        self.loginButton.setIconSize(QtCore.QSize(40, 40))
        
        # Esconder a senha
        self.linePassword.setEchoMode(QLineEdit.EchoMode.Password)

    def goToMenu(self):
        user = self.lineUser.text()
        password = self.linePassword.text()

        if len(user) == 0 or len(password) == 0:
            self.labelWrong.setText("Por favor, preencha todos os campos!")
            return  # Sai da função se algum campo estiver vazio

        if not db.isOpen():
            self.labelWrong.setText("Erro na conexão com o banco de dados!")
            return

        query = QSqlQuery()
        query.prepare("SELECT * FROM login_info WHERE username = :user")
        query.bindValue(":user", user)

        if query.exec() and query.first():  # Executa a query e verifica se há resultado
            stored_password = query.value(1)  # Supondo que a senha esteja na segunda coluna (índice 1)

            if stored_password == password:
                print("Logado com sucesso!")
                self.labelWrong.setText("")
                menu = MenuScreen()
                widget.addWidget(menu)  
                widget.setCurrentWidget(menu)  
            else:
                self.labelWrong.setText("Usuário ou senha inválida!")
        else:
            self.labelWrong.setText("Usuário ou senha inválida!")

class MenuScreen(QDialog):
    def __init__(self):
        super(MenuScreen, self).__init__()
        loadUi("menu.ui", self)  

        # Ligação com os registros
        self.signButton.clicked.connect(self.goToRegister)
        self.searchButton.clicked.connect(self.goToSearch)
        self.aboutButton.clicked.connect(self.goToAbout)

        # Ícones dos botões

        icon = QtGui.QIcon(os.path.join(icon_path, "signUp.png"))  
        self.signButton.setIcon(icon)
        self.signButton.setIconSize(QtCore.QSize(40, 40))

        icon = QtGui.QIcon(os.path.join(icon_path, "search.png"))  
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QtCore.QSize(40, 40))

        icon = QtGui.QIcon(os.path.join(icon_path, "about.png"))  
        self.aboutButton.setIcon(icon)
        self.aboutButton.setIconSize(QtCore.QSize(40, 40))

        icon = QtGui.QIcon(os.path.join(icon_path, "exit.png"))  
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(QtCore.QSize(40, 40))
        self.exitButton.clicked.connect(self.selfDestruct)
    
    def selfDestruct(self):
        print("É perigoso ir sozinho...")
        exit()

    def goToRegister(self):
        menu = RegisterScreen()
        widget.addWidget(menu)  
        widget.setCurrentWidget(menu)

    def goToSearch(self):
        menu = SearchScreen()
        widget.addWidget(menu)
        widget.setCurrentWidget(menu)

    def goToAbout(self):
        menu = AboutScreen()
        widget.addWidget(menu)
        widget.setCurrentWidget(menu)

class RegisterScreen(QDialog):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        loadUi("register.ui", self)

        self.backButton.clicked.connect(self.goToMenu)
        self.signButton.clicked.connect(self.Register)

        # Ícones
        icon = QtGui.QIcon(os.path.join(icon_path, "signUp.png"))  
        self.signButton.setIcon(icon)
        self.signButton.setIconSize(QtCore.QSize(40, 40))
        icon = QtGui.QIcon(os.path.join(icon_path, "back.png"))  
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(40, 40))

    def Register(self):
        name = self.lineName.text()
        type = self.comboBoxType.currentText()  # Corrigido para obter o texto selecionado
        fit = self.spinBoxFit.value()  # Obtém o valor inteiro correto
        stock = self.spinBoxStock.value()  # Obtém o valor inteiro correto
        price = self.doubleSpinBoxPrice.value()  # Obtém o valor flutuante correto

    # Verificando qual rádio está marcado
        if self.radioButtonF.isChecked():
            gender = "F"
        elif self.radioButtonM.isChecked():
            gender = "M"
        elif self.radioButtonX.isChecked():
            gender = "X"
        else:
            gender = None  # Caso nenhum esteja selecionado

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not name or not type or not gender or fit <= 0 or stock < 0 or price <= 0:
            self.labelWrong.setText("Por favor, preencha todos os campos corretamente!")
            return

        if not db.isOpen():
            self.labelWrong.setText("Erro na conexão com o banco de dados!")
            return

        # Inserindo no banco de dados
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO stock_info (Name, Type, Gender, Fit, Stock, Price)
            VALUES (:name, :type, :gender, :fit, :stock, :price)
            """)
    
        query.bindValue(":name", name)
        query.bindValue(":type", type)
        query.bindValue(":gender", gender)
        query.bindValue(":fit", fit)
        query.bindValue(":stock", stock)
        query.bindValue(":price", price)

        if query.exec():
            print("Registro inserido com sucesso!")
            self.labelWrong.setText("Cadastro realizado com sucesso!")
        else:
            print("Erro ao inserir no banco de dados:", query.lastError().text())
            self.labelWrong.setText("Erro ao cadastrar. Tente novamente.")


    def goToMenu(self):
        menu = MenuScreen()
        widget.addWidget(menu)  
        widget.setCurrentWidget(menu)


class SearchScreen(QDialog):
    def __init__(self):
        super(SearchScreen, self).__init__()
        loadUi("search.ui", self)

        self.searchButton.clicked.connect(self.Search)
        self.backButton.clicked.connect(self.goToMenu)

        # Ícones
        icon = QtGui.QIcon(os.path.join(icon_path, "search.png"))  
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QtCore.QSize(40, 40))
        icon = QtGui.QIcon(os.path.join(icon_path, "back.png"))  
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(40, 40))

    def Search(self):
        # Obtém os valores do campo de pesquisa e do combobox
        name = self.lineSearch.text()

        # Verifica se o banco de dados está aberto
        if not db.isOpen():
            print("Erro na conexão com o banco de dados!")
            return

        query = QSqlQuery()
        query.prepare("""
            SELECT Name, Type, Gender, Fit, Stock, Price FROM stock_info
            WHERE Name = :name
        """)

        query.bindValue(":name", name)

        if query.exec():
            results = []  # Lista para armazenar os resultados formatados
        
            while query.next():  # Percorre todas as linhas retornadas
                name = query.value(0)  # Nome
                type = query.value(1)  # Tipo
                gender = query.value(2)  # Gênero
                fit = query.value(3)  # Fit
                stock = query.value(4)  # Estoque
                price = query.value(5)  # Preço

                # Formata os dados e adiciona à lista
                results.append(f"Nome: {name}, Tipo: {type}, Gênero: {gender}, Fit: {fit}, Estoque: {stock}, Preço: R$ {price:.2f}")

            if results:
                self.textBrowser.setText("\n".join(results))  # Exibe os resultados formatados
            else:
                self.textBrowser.setText("Nenhum resultado encontrado.")

        else:
            print("Erro ao procurar no banco de dados:", query.lastError().text())

    def goToMenu(self):
        menu = MenuScreen()
        widget.addWidget(menu)  
        widget.setCurrentWidget(menu)

class AboutScreen(QDialog):
    def __init__(self):
        super(AboutScreen, self).__init__()
        loadUi("about.ui", self)

        self.backButton.clicked.connect(self.goToMenu)

        # Ícones
        icon = QtGui.QIcon(os.path.join(icon_path, "back.png"))  
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(40, 40))

    def goToMenu(self):
        menu = MenuScreen()
        widget.addWidget(menu)  
        widget.setCurrentWidget(menu)



# Configuração principal do aplicativo
widget = QtWidgets.QStackedWidget()

# Criando a tela inicial (Login)
login_screen = LoginScreen()
widget.addWidget(login_screen)

# Configurar tamanho fixo da janela
widget.setFixedHeight(480)
widget.setFixedWidth(640)

widget.show()  
sys.exit(app.exec())

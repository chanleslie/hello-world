
import webapp2 # To host the server as a web page
import cgi
import random # To designate Ts and Is
import smtplib # To send e-mails
from email.mime.text import MIMEText # To send text in e-mails
from datetime import datetime # To timestamp the current game
from tinydb import TinyDB, Query # To handle persistent data like user info and wins

currentVersion = "3"
permGameNum = "1"

# Consider creating a class to represent the current game + details
# Allows us to customize kinds of games like different messages, sleeper agents, etc.
currentUsers = []
supportedProviders = []
currentTnames = []
currentGame = []
gameTime = datetime.now()
numberTs = 3
gameNum = 1
emailUsername = 'jack8mochi@gmail.com'
emailPassword = 'mochi8jack'
userDB = TinyDB('C:\TTT\Users.json')
gamesDB = TinyDB('C:\TTT\Games.json')
gameActive = False

### E-mail stuff
innocentMessage = 'You are innocent.'
tMessage = 'You are a MAFIA. All M\'s: '
soloT = 'You are a MAFIA, '
s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login(emailUsername, emailPassword)


### End e-mail stuff

class Provider(object):
    provider = ''
    gateway = ''

    def __init__(self, providerName, gatewaySuffix):
        self.provider = providerName
        self.gateway = gatewaySuffix

def reconnect():
    global s
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(emailUsername, emailPassword)



def sendMessage(user=None, msgStatus='start'):
#can also do case switch statements
    if msgStatus == 'start':
        now = gameTime
        #preamble = 'For the game on ' + '/'.join([str(now.month), str(now.day), str(now.year)]) + ' starting at ' + ':'.join([str(now.hour), str(now.minute), str(now.second), str(now.microsecond)]) + '\n'
        preamble = 'Game# ' + str(gameNum) + ('; There is 1 MAFIA' if numberTs <= 1 else '; There are ' + str(numberTs -1) + '-' + str(numberTs) + ' MAFIA')+ ' : '
        global currentTnames
        traitorMessage = soloT if len(currentTnames) == 1 else tMessage
        if user != None:
            if user.status == 'T':
                msg = MIMEText(preamble + user.name + ', ' + traitorMessage + ', '.join(currentTnames))
            else:
                msg = MIMEText(preamble + user.name + ', ' + innocentMessage)

    if msgStatus == 'newPlayerTest':
        msg = MIMEText('WELCOME TO MAFIA.')

    if msgStatus == 'confirmCurrentPlayers':
        msg = MIMEText('You are enrolled for the next game session.')

    try:
        msg['To'] = user.number + user.provider.gateway
        s.sendmail(emailUsername, msg['To'], msg.as_string())
        print 'Message sent to ' + user.name

    except:
        print 'Message failed, re-connecting'
        reconnect()

        try:
            s.sendmail(emailUsername, msg['To'], msg.as_string())
            print 'Retry Successful, Message sent to ' + user.name

        except:
            print 'Message Failed, Restart Server'


#if chance of wanting to change T selection, create flag or button selection method
def connorTs(curUsers): #for up-to # T's
    pass
    global numberTs
    global currentTnames

    for _ in range(numberTs):
        t = random.randrange(0,len(curUsers))
        if curUsers[t].status is 'T':
            curUsers[t].status = 'T'
            currentTnames.append(curUsers[t].name)

def setNumTs(curUsers): #Set value gurantees number of T's
    pass
    global numberTs
    global currentTnames
    counter = 0

    if len(curUsers) < numberTs:
        numberTs = 0

    while counter < numberTs:
        t = random.randrange(0, len(curUsers))
        if curUsers[t].status is 'T':
            continue
        else:
            curUsers[t].status = 'T'
            currentTnames.append(curUsers[t].name)
            counter += 1

def lessT(curUsers): #Example: If 2, range of 1 or 2; 3 is range of 2-3. Set for 30%
    pass

    global numberTs
    global currentTnames
    nTs = numberTs

    if len(curUsers) < numberTs:
        numberTs = 0
    randomp = random.random()
    #print randomp
    if numberTs > 1:
        if randomp < .3:
            nTs = numberTs - 1

        counter = 0


        while counter < nTs:
            t = random.randrange(0, len(curUsers))
            if curUsers[t].status is 'T':
                continue
            else:
                curUsers[t].status = 'T'
                currentTnames.append(curUsers[t].name)
                counter += 1


def generateGame(curUsers):
    #consider making copy of curUsers for currentTnames
    #as is code still may text an innocent who are T

    global gameTime
    gameTime = datetime.now()

    for user in curUsers:
        user.status = ''

    global currentTnames
    global numberTs

    lessT(curUsers)


    #Code below is same as setTs
##    counter = 0
##
##    if len(curUsers) < numberTs:
##        #print len(curUsers)
##        print numberTs
##        numberTs = 0
##
##    while counter < numberTs:
##        t = random.randrange(0, len(curUsers))
##        if curUsers[t].status is 'T':
##            continue
##        else:
##            curUsers[t].status = 'T'
##            currentTnames.append(curUsers[t].name)
##            counter += 1





    currentTnames = list(set(currentTnames))

    return curUsers

class Game(object):
    victors = "" # One of [T, I]
    traitors = []
    innocents = []

    def __init__(self, allPlayers, currentTraitors):
        for player in allPlayers:
            if player in currentTraitors:
                traitors .append(player)
            else:
                innocents .append(player)


    def setVictor(self, winner):
        ### UNUSED INFO
        if winner in ["T", "I"]:
            self.victors = winner

    def asDict(self):
        return {'winners' : self.victors}


class User(object):
    name = ''
    number = ''
    status = ''
    provider = Provider('', '')
    tWins = 0
    iWins = 0

    def __init__(self, name = '', number = '', status = '', tWins = 0, iWins = 0, provider = Provider('', '')):
        self.name = name
        self.number = number
        self.status = status
        self.provider = provider
        self.tWins = tWins
        self.iWins = iWins

    def asDict(self):
        return {'name' : self.name, 'number' : self.number, 'status' : self.status, 'tWins' : self.tWins, 'iWins' : self.iWins, 'provider' : self.provider.__dict__}

    def __eq__(self, other):
        return self.asDict() == other.asDict()

    def addWin(self, player):
        if player.status == 'T':
            self.tWins += 1
        elif player.status == '':
            self.iWins += 1

        commitUserToDatabase(player)



def initializeUsers():
    pass


def initializeProviders():
    supportedProviders.append(Provider('AT&T', '@txt.att.net'))
    supportedProviders.append(Provider('Boost Mobile', '@myboostmobile.com'))
    supportedProviders.append(Provider('Metro PCS', '@mymetropcs.com'))
    supportedProviders.append(Provider('Sprint', '@messaging.sprintpcs.com'))
    supportedProviders.append(Provider('T-Mobile', '@tmomail.net'))
    supportedProviders.append(Provider('US Cellular', '@email.uscc.net'))
    supportedProviders.append(Provider('Verizon', '@vtext.com'))
    supportedProviders.append(Provider('Cricket', '@sms.mycricket.com'))
    supportedProviders.append(Provider('E-MAIL', ''))

class StartGame(webapp2.RequestHandler):
    def get(self):
        global gameActive
       #if self.request.get('numTs') is not None:
       # numberTs = int(self.request.get('numTs'))
        #print gameActive
        if not gameActive:
            global currentTnames
            currentTnames = []

            global currentGame
            global gameNum

            if len(currentUsers):
              currentGame = generateGame(currentUsers)

              for player in currentGame:
                sendMessage(player)

              self.response.out.write('Game# ' + str(gameNum) + ': Messages are now sent to each player.')
              gameNum = gameNum  + 1
              gameActive = True

            else:
              self.response.out.write('No Players')



            self.response.out.write("""
                  <html>
                      <body>
                   <form action="/startgame">
                    <input type="submit" value="Score" />
                    </form>""")

            self.response.out.write("""
                  <html>
                      <body>
                   <form action="/">
                    <input type="submit" value="Homepage" />
                    </form>""")
        else:
            self.response.out.write("""
                  <html>
                      <body>
                   <form action="/startgame" method="post">
                   <select name="Winners">
                    <option value='T'>MAFIA won</option>
                    <option value=''>Innocents won</option>
                    <option value="Cancelled">Game was cancelled</option>
                    <input type="submit" value="End game">
                    </form>""")


    def post(self):
        global gameActive
        if not gameActive:
            global numberTs
            try:
              numberTs = int(self.request.get('numTs'))
              self.redirect("/startgame")
            except:
              self.response.out.write('Please enter a valid number.')

        else:
            gameActive = False
            for player in currentGame:
##                if player.status == self.request.get("Winners"):
##                    player.addWin()
                if player.status == self.request.get("Winners"):
                    # O(n^2) again, but too small to care
                    for realPlayerObject in currentUsers:
                        if player.number == realPlayerObject.number:
                            realPlayerObject.addWin(player)
            self.redirect("/")



class AddUserPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
            <body>
              First form is player name; second form is phone number (10 Digit).
              <form action="/sign" method="post">
                <div><input type = "text" name="Player" rows="1" cols="30"></div>
                <div><input type = "text" name="Number" rows="1" cols="20"></div><select name="Provider">""")

        for provider in supportedProviders:
            self.response.out.write("""<option value=\""""
                                    + provider.provider.split()[0].lower()
                                    + """\">""" + provider.provider
                                    + """</option>""")

        self.response.out.write("""</select>
                <div><input type="submit" value="Add new user"></div>
              </form>
            </body>
          </html>""")

        #update user name
        self.response.out.write('Change User Nickname')
        self.response.out.write("""
          <html>
            <form action="/chi" method="post">
               </div><select name="User">""")

        for user in userDB.all():
            self.response.out.write("""<option value=\""""
                                    + user['number']
                                    + """\">""" + user['name']
                                    + """</option>""")

        self.response.out.write('<div><input type = "text" name="nick" rows="1" cols="30"></div>')


        self.response.out.write("""</select>
                <div><input type="submit" name="Change" value="Change Name"></div>
              </form>
            </body>
          </html>""")

    def post(self):
        player = User()
        query = Query()
        nick = self.request.get('nick')
        #print self.request.get('User')
        if self.request.get('nick') != '':
            userDB.update({'name': nick}, query.number == self.request.get('User'))

        self.redirect('/chi')




def refreshDatabase():
    player = User()
    for user in userDB.all():
        player = buildUserFromDict(user)
        commitUserToDatabase(player)


class DeleteUserPage(webapp2.RequestHandler):
     def get(self):
        self.response.out.write("""
          <html>
            <form action="/deleted" method="post">
               </div><select name="User">""")

        for user in currentUsers:
            self.response.out.write("""<option value=\""""
                                    + str(currentUsers.index(user))
                                    + """\">""" + user.name
                                    + """</option>""")


        self.response.out.write("""</select>
                <div><input type="submit" name="Delete" value="Delete user"></div>
                <div><input type="submit" value="Resend recent text"></div
              </form>
            </body>
          </html>""")

def commitUserToDatabase(player):
    if not userDB.get(Query().number == player.number):
      userDB.insert(player.asDict())
    else:
      userDB.update(player.asDict(), Query().number == player.number) # This updates things including those that aren't updated often (name, number). Maybe add a function to user for the stats worth updating (score, etc.)
    print userDB.all()

class NewGuestbook(webapp2.RequestHandler):
    def post(self):

        index = self.request.get('User')
        #print index

        global currentUsers


        if len(currentUsers):
          if self.request.get('Delete'):
            removePlayerFromSession(currentUsers[int(index)])
            self.response.out.write('User Deleted')
          else:
            if len(currentGame):
              sendMessage(currentGame[int(index)])
              self.response.out.write('Resent game to ' + currentGame[int(index)].name)
            else:
              self.response.out.write('No game to resend.')
        else:
          self.response.out.write('No user with which to do anything.')

        self.response.out.write("""
              <html>
                  <body>
               <form action="/">
                <input type="submit" value="Homepage" />
                </form>""")

def addPlayerToSystem(player):
        commitUserToDatabase(player)
        currentUsers.append(player)
        sendMessage(player, 'newPlayerTest')

class ResendToAll(webapp2.RequestHandler):
    def get(self):
        for player in currentUsers:
            sendMessage(player, 'confirmCurrentPlayers')
        self.redirect('/')


class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write('<br />New player is ' + cgi.escape(self.request.get('Player')))
        self.response.out.write('<br />Player\'s phone number is ' + cgi.escape(self.request.get('Number')))
        self.response.out.write('</pre></body></html>')
        player = User()
        player.name = self.request.get('Player')
        player.number = self.request.get('Number')

        for provider in supportedProviders:
            if provider.provider.split()[0].lower() == self.request.get('Provider'):
                player.provider = provider

        self.response.out.write(player.name)
        addPlayerToSystem(player)

        self.response.out.write("""
              <html>
                  <body>
               <form action="/">
                <input type="submit" value="Homepage" />
                </form>""")

class PlayerList(webapp2.RequestHandler):
    def get(self):
        u = Query()
        self.response.out.write("""<table id="why" style="width:65%">
            <tr><th>Willing to Play</th><th>Name</th><th>Phone Number</th><th>Innocent Wins</th><th>MAFIA Wins</th><th>Total</th></tr>
            """)
        self.response.out.write('<form action="/playerlist" method="post">')
        for user in userDB.all():
            #self.response.out.write('<br />' + user['name'] + '\t\t\t' + user['number'])
            self.response.out.write('<tr> <td align="center"><input type="checkbox" name="' + user['number'] + '" value="test"'
                                    + (' checked="true"' if buildUserFromDict(user) in currentUsers else '') +'></td>'
                                    + '<td align="center">' + user['name'] + '</td><td align="center">' + user['number'] + '</td><td align="center">'
                                    + str(user['iWins']) + '</td><td align="center">' + str(user['tWins'])
                                    + '</td><td align="center">' + str(user['tWins'] + user['iWins'])
                                    + '</td></input></tr>')
                                   # + user['name'] + '\t\t\t' + user['number'] + '</input><br />')
        self.response.out.write('</table><br /><br /><input type="submit" value="Submit"/></form><br />')
       # print userDB.get(u.name=='Alex')['number']

        if len(currentUsers):
            self.response.out.write('Current Players are: <br />')

        for user in currentUsers:
            self.response.write(user.name + '<br />')

        self.response.out.write("""
              <html>
                  <body><br /><br />
               <form action="/">
                <input type="submit" value="Homepage" />
                </form>""")


    def post(self):
        player = User()
        # Currently O(n^2), maybe can fix with a try{}expect for the else
        for user in userDB.all():
            if self.request.get(user['number']):
                currentPlayer = buildUserFromDict(user)
                if currentPlayer not in currentUsers:
                    currentUsers.append(currentPlayer)
            else:
                currentPlayer = buildUserFromDict(user)
                if currentPlayer in currentUsers:
                    removePlayerFromSession(currentPlayer)

        self.get()

class Leaderboard(webapp2.RequestHandler):
    pass



def buildUserFromDict(userDict):
    try:
        return User(name=userDict['name'], number = userDict['number'], tWins = userDict['tWins'], iWins = userDict['iWins'], provider = Provider(userDict['provider']['provider'], userDict['provider']['gateway']))
    except:
        return User(name=userDict['name'], number = userDict['number'], provider = Provider(userDict['provider']['provider'], userDict['provider']['gateway']))

def removePlayerFromSession(userObj):
    commitUserToDatabase(userObj)
    currentUsers.remove(userObj)



class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        # for i in range(1,100):
            # self.response.write('Hi!<br />')

        self.response.write('Welcome to the MAFIA Server. Time for Darkness, Deception and Death. If you do not comply, KYS.' + '<br />' + '<br />')

        self.response.write('Set Max Number of Mafia\'s, Current set to ' + str(numberTs) + '<br />')

        self.response.write("""
          <html>
              <body>
           <form action="/startgame" method="post"><div><input type = "text" name="numTs" size="1">
            <input type="submit" value="Change and Start" /></div></form>""")


        for user in currentUsers:
            self.response.write(user.name + ' has a number of ' + user.number + '<br />')
            self.response.write('Their provider is ' + user.provider.provider + '<br />' + '<br />')

        self.response.out.write("""
          <html>
              <body>
           <form action="/chi">
            <input type="submit" value="Add New User/ Change Nickname" />
            </form>""")

        self.response.out.write("""
          <html>
              <body>
           <form action="/eyob">
            <input type="submit" value="Delete User / Resend Text" />
            </form>""")

        self.response.out.write("""
          <html>
              <body>
           <form action="/playerlist">
            <input type="submit" value="Add Players from List" />
            </form>""")

        self.response.out.write("""
          <html>
              <body>
           <form action="/resendtoall">
            <input type="submit" value="Text to Confirm CurrentPlayers" />
            </form>""")


        self.response.out.write("""
          <html>
              <body>
           <form action="/startgame">
            <input type="submit" value="Start Game" />
            </form>""")

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/chi', AddUserPage),
    ('/eyob', DeleteUserPage),
    ('/sign', Guestbook),
    ('/deleted', NewGuestbook),
    ('/startgame', StartGame),
    ('/playerlist', PlayerList),
    ('/resendtoall', ResendToAll),
], debug=True)

def checkForUpdates():
    try:
        log = open('C:\Temp\TTTlog', 'r+')
    except:
        log = open('C:\Temp\TTTlog', 'w+')
    log.seek(0)
    if log.read() != currentVersion:
        log.seek(0)
        log.write(currentVersion)
        refreshDatabase()
    log.close()

def readGameNum():
    global gameNum
    global permGameNum

    try:
        log = open('C:\Temp\TTTlogGame', 'r+')
    except:
        log = open('C:\Temp\TTTlogGame', 'w+')
        log.write(str(gameNum))
        return 0


    log.seek(0)
    print 'reading gamenum'
    gameNum = int(log.read())

    log.close()

def writeGameNum():
    global gameNum
    global permGameNum

    try:
        log = open('C:\Temp\TTTlogGame', 'w+')
    except:
        print 'write failed'

    log.seek(0)
    log.write(str(gameNum))
    log.close()




def endGame(currentGame, winners):
    if currentGame:
        gamesDB.insert(currentGame.asDict())

def exitProgram():
    userDB.close()
    gamesDB.close()
    writeGameNum()
    s.quit()

def main():
    from paste import httpserver
    initializeProviders()
    #initializeUsers() # use to preload people with no db
    httpserver.serve(app, host='0.0.0.0', port='3000')

if __name__ == '__main__':
    checkForUpdates()
    readGameNum()
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exitProgram()

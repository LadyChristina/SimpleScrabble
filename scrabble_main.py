import pickle
import datetime
import myLib as ml

''' Εμφανίζει το μενού στο χρήστη και επιστρέφει την επιλογή του. '''
def menu():
    print('~S C R A B B L E~')
    print('1. Παιχνίδι')
    print('2. Ρυθμίσεις')
    print('3. Σκορ')
    print('4. Έξοδος')
    print()
    choice=input('Τι επιλέγεις? ')
    print()
    return choice

''' Φορτώνει τα σκορ σε ένα λεξικό και το επιστρέφει. '''
def loadScores():
    try:
        with open('scores.pkl','rb')as sc:
            scores = pickle.load(sc) 
    except IOError:
        with open('scores.pkl','wb') as sc:
            #αν δεν υπάρχει το αρχείο (πρακτικά την πρώτη φορά που παίζει ο παίκτης), το δημιουργούμε
            scores = {}
    except EOFError:
        #κενό αρχείο
        scores = {}
    return scores

''' Αποθηκεύει τα σκορ σε pickle σε μορφή λεξικού {αύξων αριθμός: [ημερομηνία,σκορ υπολογιστή, σκορ ανθρώπου]}. '''
def dumpScores(score1,score2,scores):
    d = datetime.date.today()
    scores[len(scores)]=[d,score1,score2]
    with open('scores.pkl','wb') as sc:
        pickle.dump(scores,sc)

''' Εναλλάσει τη σειρά του χρήστη με του υπολογιστή και καλέι τη συνάρτηση για το τέλος του παιχνιδιού. '''
def exchangeTurns(sak, human, computer,mode):
    while True:        
        print('-----------------------------')
        sak.print_size()        
        print('-----------------------------')
        human.turn(sak,dictionary,mode)
        if human.quit==True:
            print_final(human,computer)
            break
        print('-----------------------------')
        sak.print_size()        
        print('-----------------------------')
        computer.turn(sak,dictionary,mode)
        if computer.quit==True: 
            print_final(human,computer)
            break

''' Διαχειρίζεται το τέλος του παιχνιδιού. '''
def print_final(human,computer):
    print ('To σκορ σου είναι:',human.score)
    print ('Το σκορ του υπολογιστή είναι:',computer.score)
    if human.score>computer.score:
        print('\nΣυγχαρητήρια! Κέρδισες!')
    elif human.score==computer.score:
        print('\nΙσσοπαλία!')
    else:
        print('\nΛυπάμαι...Έχασες!')
    print()



    
##### main ######
dictionary = ml.GreekDictionary()
scores = loadScores()
choice=menu()
mode=2 #αρχικοποιούμε το βαθμό δυσκολίας του υπολογιστή στο MAX LETTERS
while choice!='4':
    if choice=='1': # παιχνίδι
        mySak = ml.SakClass();
        human = ml.PlayerClass(mySak,True)
        computer = ml.PlayerClass(mySak)
        exchangeTurns(mySak, human, computer,mode)        
        dumpScores(human.score,computer.score,scores)
    elif choice=='2':
        #ρυθμίσεις: επίπεδο δυσκολίας του υπολογιστη
        mode=0
        while (mode!=1 and mode!=2 and mode!=3):
            print ('Επίπεδο δυσκολίας του υπολογιστή:')
            print ('1. Εύκολο') #min letters
            print ('2. Μέτριο') #max letters
            print ('3. Δύσκολο') #smart
            mode=input('Επιλογή: ')
            try:
                mode=int(mode)
            except ValueError:
                pass
            print()
    elif choice=='3': # σκορ
        print ('-----------------------------')
        print ('Σκορ')
        print ('-----------------------------')
        print ('Ημερομηνία', 'Σκορ Παίκτη', 'Σκορ Υπολογιστή')
        for i in sorted(scores.keys(), reverse=True):
            d=scores[i][0]
            d=d.strftime("%d/%m/%Y")
            score1=scores[i][1]
            score2=scores[i][2]
            print ("{}\t{}\t{}".format(d, score1, score2))
        print()
    choice=menu()
print ('Αντίο!') # έξοδος

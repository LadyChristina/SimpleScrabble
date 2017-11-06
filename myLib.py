import random as rn
import itertools as it
import pickle

''' Αναπαριστά το σακουλάκι με τα γράμματα του παιχνιδιού και διαχειρίζεται τα γράμματα των παικτών.
lets-> λεξικό με όλα τα διαθέσιμα γράμματα, το πλήθος του καθενός και η αξία του.
letlist-> λίστα με όλα τα διαθέσιμα γράμματα '''
class SakClass:
    ''' Αναπαριστά το σακουλάκι με τα γράμματα του παιχνιδιού και διαχειρίζεται τα γράμματα των παικτών.
    lets-> λεξικό με όλα τα διαθέσιμα γράμματα, το πλήθος του καθενός και η αξία του.
    letlist-> λίστα με όλα τα διαθέσιμα γράμματα '''
    
    def __init__(self):
        self.lets = {'Α':[12,1],'Β':[1,8],'Γ':[2,4],'Δ':[2,4],'Ε':[8,1],
         'Ζ':[1,10],'Η':[7,1],'Θ':[1,10],'Ι':[8,1],'Κ':[4,2],
         'Λ':[3,3],'Μ':[3,3],'Ν':[6,1],'Ξ':[1,10],'Ο':[9,1],
         'Π':[4,2],'Ρ':[5,2],'Σ':[7,1],'Τ':[8,1],'Υ':[4,2],
         'Φ':[1,8],'Χ':[1,8],'Ψ':[1,10],'Ω':[3,3]
         }
        self.randomize_sak()

    ''' Τοποθετεί όλα τα διαθέσιμα γράμματα σε τυχαια σειρά '''
    def randomize_sak(self):
        self.letlist = [ ]
        for key in self.lets:
            for i in range (self.lets[key][0]):
                self.letlist.append(key)
        rn.shuffle(self.letlist)

    ''' Τραβάει n γράμματα από το σακουλάκι '''
    def getletters(self,n):
        getlets=[]
        remaining=len(self.letlist)
        if n<=remaining:
            getlets=rn.sample(self.letlist,n)
            for i in getlets:
                if self.lets[i][0]>0:
                    self.lets[i][0]-=1
            self.randomize_sak()
        elif remaining!=0:
            #το σακουλάκι δεν έχει αρκετά γράμματα, δίνουμε όσα έχει
            getlets=rn.sample(self.letlist,remaining)
            for i in getlets:
                if self.lets[i][0]>0:
                    self.lets[i][0]-=1
            self.randomize_sak()
        return getlets

    ''' Τοποθετεί γράμματα πίσω στο σακουλάκι '''
    def putbackletters(self,backlets):
        for i in backlets:
            self.lets[i][0]+=1
        self.randomize_sak()

    ''' Εκτυπώνει πόσα γράμματα υπάρχουν μες στο σακουλάκι '''
    def print_size(self):
        print("Ο σάκος περιέχει ",end="")
        print(sum(self.lets[k][0] for k in self.lets),end="")
        print (" γράμματα.")

    ''' Ελέγχει αν η λέξη που δόθηκε παράγεται από τα γράμματα του χρήστη '''
    def check_letters(self,given_letters,given_word):
        letters=list(given_letters) #κάνουμε αντιγραφο της λίστας για να μην την επηρεάσουμε
        for letter in given_word:
            if letter.upper() in letters:
                letters.remove(letter.upper())
            else:
                return False
        return True


class PlayerClass():    
    ''' Αναπαριστά τους παίκτες, δηλαδή τον χρήστη και τον υπολογιστή. 
    Επιλέξαμε να τελειώνει το παιχνίδι όταν τελειώσουν τα γράμματα ενός παίκτη (και όχι όταν τελιώσουν τα γράμματα απ' το σακουλάκι που προτεινει ο οδηγός εργασίας).
    Επομένως, ένας παίχτης θα μπορεί να παίξει με λίγότερα από 7 γράμματα όταν το σακουλάκι δεν έχει γράμματα για να ενημερώσει τα γράμματα του παίχτη.
    letters-> λίστα με τα γράμματ του παίχτη
    isHuman-> boolean που ορίζει να ο παίχτης είναι άνθρωπος (χρήστης) ή όχι (υπολογιστής)
    quit-> boolean που αν είναι True δηλώνει το τέλος του παιχνιδιού
    score-> το σκορ του παίχτη'''

    def __init__(self,sak,isHuman = False):
        self.letters=[ ] 
        self.getletters(sak.getletters(7)) #η πρώτη φορά που παίρνει γράμματα ο κάθε παίκτης
        self.isHuman = isHuman
        self.quit=False
        self.score=0 #αρχικοποίηση των βαθμών κάθε παίκτη

    ''' Ανάλογα με το ποιανού η σειρά είναι, καλει την αντίστοιχη συνάρτηση. '''
    def turn(self,sak,dictionary,mode):
        if self.isHuman:
            print('Σειρά σου') 
            self.humansTurn(sak,dictionary)
        else:
            self.computersTurn(sak,dictionary,mode)

    ''' Ενημερώνει τα γράμματα του παίκτη. '''  
    def getletters(self,letters):
        self.letters+=letters

    ''' Εμφανίζει τα διαθέσιμα γράμματα του παίκτη μαζί με την αξία του κάθε γράμματος. '''   
    def printletters(self,sak):
        print ('Διαθέσιμα Γράμματα: ', end='')
        for key in self.letters:
            print ((str(key),sak.lets[key][1]),end=' ')

    ''' Παίζει ο χρήστης. Το πρόγραμμα ζητάει από τον χρήστη μια λέξη από τα διαθέσιμά του γράμματα και κάνει τους κατάλληλους ελέγχους και αιτήματα για να λάβει έγκυρη λέξη. '''
    def humansTurn(self,sak,dictionary):   
        self.printletters(sak)
        word=input("\nΌποτε θες πληκτρολόγησε 'p' για να πας πάσο και να αλλάξεις γράμματα ή 'q' για να λήξει η παρτίδα. \nΛέξη: " )
        while word!='q' and word!='flag' and word!='p':
            if (sak.check_letters(self.letters,word)) == False:
                print ("Παρακαλώ να χρησιμοποιείς μόνο τα γράμματά σου!")
                self.printletters(sak)
                word=input("\nΛέξη: " )
            else:
                points = dictionary.getpoints(word)
                if points==-1: #η λέξη δεν υπάρχει στο λεξικό
                    print ("Μη έγκυρη λέξη!")
                    self.printletters(sak)
                    word=input("\nΛέξη: " )
                else:
                    print('Αποδεκτή λέξη \nΒαθμοί: ',points)
                    self.score+=points
                    print('Σύνολο: ', self.score)
                    enter=input('Enter για συνέχεια')
                    self.throwLetters(word)
                    self.getletters(sak.getletters(len(word)))
                    if not self.letters: #τελείωσαν τα γράμματα του παίκτη
                        print ('Τα γράμματά σου τελείωσαν! Τέλος παρτίδας!')
                        self.quit=True
                    word='flag'
        if word=='q':
            self.quit=True
        if word=='p':
            #ο παίκτης επιλέγει να αλλάξει τα γράμματά του, οπότε χάνει τη σειρά του
            print()
            sak.putbackletters(self.letters)
            del self.letters[:]
            self.getletters(sak.getletters(7))
            #αν δεν υπάρχουν άλλα γράμματα στο σακουλάκι, ο παίκτης απλως ξαναπαίρνει τα ίδια γράμματα
        print()

    ''' Αφαιρεί τα γράμματα που χρησιμοποιήθηκαν για τη δημιουργία λέξης από τα διαθέσιμα γράμματα του παίκτη. '''                                
    def throwLetters(self,lets):
        for l in lets:
            try:
                self.letters.remove(l.upper())
            except ValueError:
                pass

    ''' Παίζει ο υπολογιστής. Καλεί συνάρτηση που δημιουργεί τη λέξη του και την επιστρέφει μαζί με τους πόντους της και τα εμφανίζει στο χρήστη. '''
    def computersTurn(self,sak,dictionary,mode):
        print('Σειρά του Υπολογιστή')
        self.printletters(sak)
        word,points=self.makepermutations(dictionary,mode)
        if (word==-1 and points==-1):
            print("Ο Υπολογιστής δε βρήκε λέξη! Τέλος παρτίδας!")
            self.quit=True
            return
        print('\nΛέξη: ',word)
        print('Βαθμοί: ',points)
        self.score+=points
        print('Σύνολο: ', self.score)
        self.throwLetters(word)
        self.getletters(sak.getletters(len(word)))
        if not self.letters: #τελείωσαν τα γράμματα του υπολογιστή
            print ('Τα γράμματα του υπολογιστή τελείωσαν! Τέλος παρτίδας!')
            self.quit=True
        print()

    ''' Δημιουργεί λέξη για τον υπολογιστή, ανάλογα με το mode που έχει ορίσει ο χρήστης από τις ρυθμίσεις.
    Διαθέσιμα modes: 1 = minletters, 2 = maxletters, 3 =smart
    Αρχικοποιείται mode=2 '''
    def makepermutations(self,dictionary,mode):
        found = False
        if mode==3: #smart
            maxpoints=0
            for i in range(1,len(self.letters)+1,1):
                for perm in it.permutations(self.letters,i):
                    perm="".join(list(perm))
                    if dictionary.getpoints(perm)!=-1 and dictionary.getpoints(perm)>maxpoints:
                        found= True
                        maxpoints=dictionary.getpoints(perm)
                        word=perm
        else:
            if mode==1: #min letters
                x,y,z = 1,len(self.letters)+1,1
            else: #mode==2: max letters
                x,y,z = len(self.letters),0,-1
            for i in range(x,y,z):
                for perm in it.permutations(self.letters,i):
                    perm="".join(list(perm))
                    if dictionary.getpoints(perm)!=-1:
                        return perm,dictionary.getpoints(perm)
        if found==True: #mode=3
            return word,maxpoints
        else:
            return -1,-1

class GreekDictionary:
    ''' Φορτώνει το αρχείο greek7.pkl που έχει μέσα ένα λεξικό με τις λέξεις 2 έως 7 γραμμάτων και τους πόντους τους. '''        
    def __init__(self):
        try:
            with open('greek7.pkl','rb') as gr:
                self.points=pickle.load(gr)
        except IOError:
            print('Το αρχειο greek7.pkl δε βρέθηκε!')
            
    ''' Επιστρέφει τους πόντους της δοθείσης λέξης ή -1 αν η λέξη δεν υπάρχει στο λεξικό.'''
    def getpoints(self,word):
        return self.points.get(word.upper(),-1)

from tkinter import*
from tkinter.ttk import*
from tkinter import messagebox
class Product:

    attributes = ['product_id', 'product_name','unit_price','items_in_stock','thumb']
    attributesDisplay = {'product_id': 'Product ID', 'product_name':'Product Name','unit_price':'Unit Price','items_in_stock':'Items in Stock','thumb':'thumbnail'}
    productDict = {}
    def __init__(self, product_id, product_name, price, stocks,thumbLoc):
        self.product_id = product_id
        self.product_name = product_name
        self.unit_price = price
        self.items_in_stock = stocks
        self.thumb = thumbLoc
        
        

    def fetchProductDict(self):
        
        with open('productsfile.txt','r') as productFile:
            for prod in productFile:
                prod = prod.split()
                
                self.productDict[prod[0]] = Product(prod[0], prod[1], float(prod[2]), int(prod[3]), prod[4] )


            
    def writeProductDict2File(self):
        with open('productsfile.txt','w') as productFile:
            for product in self.productDict:
                line=''
                for attribute in self.attributes:
                    line += str(getattr(self.productDict[product],attribute))
                productFile.write(line)
                    

#    def saveNewProduct(self):
 #       with open('productsfile.txt','a') as productFile:
  #          productFile.write(self.product_id, self.product_name, self.thumb, self.unit_price, self.items_in_stock, self.valid)
    
   # def removeProduct(self):
    #    with open('productsfile.txt','w+') as productFile:
     #       prodLst = productFile.readlines()
      #      for prod in prodLst:
       #         if self.product_id in prod[0]:
        #            prod = prod[:-5] + 'False\n'
         #   productFile.writelines(prodLst)
            

class Cart(Product):

    def __init__(self):
        self.item_dict = {}
        self.cart_bill = 0

    def addItem(self, product_id):
        if product_id in self.item_dict:
            self.item_dict[product_id]+=1
        else:
            self.item_dict[product_id] = 1

    def delItem(self,product_id):
        self.item_dict[product_id] = 0

    def calcCartBill(self):
        total=0
        for item in self.item_dict:
            total += self.item_dict[item]*self.productDict[item].unit_price
        self.cart_bill = total


class Account(Cart, Product):

    def __init__(self, username, password, permissions = 'customer'):

        self.username = username
        self.password = password
        self.permissions = permissions
    
    def sign_in(self):

        with open('accounts.txt','r') as accFile:
            for acc in accFile:
                acc1 = acc.split(' ').strip('\n')
                
                if self.username == acc1[0]:
                    if self.password == acc1[1]:
                        self.authStat = acc1[2]           # auth successful so get permission info too
                        return
            self.authStat = False                    # auth failed
        

    def create_account(self):

        with open('accounts.txt', 'a') as accFile:
            accFile.write([self.username, self.password,self.permissions])

class GUIRouter(Tk):

    frames={}
   
    def __init__(self):
        super().__init__()
        #self.minsize(300,200)
        #self.maxsize(600,400)
        mainContainer = Frame(self)
        mainContainer.pack(side='top', fill='both', expand= True)
        mainContainer.grid_rowconfigure(0, weight = 1)
        mainContainer.grid_columnconfigure(0, weight = 1)
        #self.frames={}
        for F in (AuthScreen,adminScreen,customerScreen,DisplayCart):
            frame = F(mainContainer,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky = 'nsew')
        self.show_frame(AuthScreen)
        
    def show_frame(self,container):
        frame= self.frames[container]
        frame.tkraise()


class AuthScreen(Account,Frame,Tk):

    def __init__(self,r,controller):
        Frame.__init__(self,r)
        self.controller = controller
        self.createForm()
        
        
        

    def createForm(self):
        Label(self, text = 'Username').grid(row=0)
        Label(self, text = 'Password').grid(row=1)
        self.e1 = Entry(self)
        self.e1.grid(row=0,column=1)
        self.e2 = Entry(self)
        self.e2.grid(row=1,column=1)
        self.authLabel = Label(self)
        self.authLabel.grid(row=3, columnspan=2)
        Button(self, text = 'Sign In', command = self.signInProcess).grid(row=2)

    def signInProcess(self):
            username = self.e1.get()
            password = self.e2.get()
            if username and password:
                Account.__init__(self, self.e1.get(), self.e2.get())
                self.sign_in()
                if self.authStat:

                    if self.authStat=='business_owner':
                        self.controller.show_frame(adminScreen)
                    elif self.authStat=='customer':
                        self.controller.show_frame(customerScreen)
                    else:
                        messagebox.showerror(title = 'Error',message='Authentication error.')

                else:
                    self.authLabel.config(text='Please enter a correct username and password')
            else:
                self.authLabel.config(text = 'Please enter a username and password')
            

    
        



class adminScreen(Frame,Product,Tk):

    def __init__(self,r, controller):
        #self.userScreen=super().__init__(r)
        Frame.__init__(self,r)
        self.fetchProductDict()
        Label(self, text='Select a product\'s ID to access its details :').grid(row=1,column=0)
        productIDstuple =  tuple([key for key in self.productDict])
        self.productIDs = Combobox(self, values = productIDstuple)
        self.productIDs.set(productIDstuple[0])
        self.productIDs.grid(row=1, column =1)
        self.makeForm()
        self.fillForm()
        



    def makeForm(self):
        attributes=['product_name','unit_price','items_in_stock','thumb']
        Label(self, text = 'Product ID').grid(row=2,column=0)
        self.productIDentry = Entry(self)
        self.productIDentry.insert(0,str(self.productIDs.get()))
        self.productIDentry.configure(state='readonly')
        self.productIDentry.grid(row = 2, column=1)
        self.entries = []
        r=3
        for field in attributes:

            lab = Label(self, text=self.attributesDisplay[field])
            lab.grid(row=r, column=0)
            ent = Entry(self)
            ent.grid(row=r, column=1)
            self.entries.append((field,ent))
            r+=1
        Button(self, text='Save', command=self.fetchEntries).grid(row = r, column=0)
        Button(self, text='Delete', command=self.deleteProduct).grid(row=r, column=1)

    def fillForm(self):

        for entry in self.entries :
            entry[1].insert(0,getattr(self.productDict[self.productIDs.get()],entry[0]))
        
    def fetchEntries(self):

        for entry in self.entries:
            setattr(self.productDict[self.productIDentry.get()],entry[0],entry[1].get())

    def deleteProduct(self):
        answer = messagebox.askyesno("Confirmation","Do you really want to delete the product permanently?")
        if answer:
            self.productDict.pop(self.productIDentry.get())
        self.writeProductDict2File()

    def addNewProduct(self):
        
        self.makeForm()
        self.fetchEntries()
        self.writeProductDict2File()
        Button(self, text='Cancel', command=self.fillForm).grid(row=10,column=1)

class customerScreen(Frame,Tk,Cart):

    def __init__(self,r,controller):
        #super().__init__(self)
        Frame.__init__(self,r)
        Cart.__init__(self)
        Button(self, text='Go to Cart', command = lambda : controller.show_frame(DisplayCart)).pack()
        self.fetchProductDict()
        self.displayCatalogue()
    
    def displayCatalogue(self):
        catalogue = Frame(self)
        catalogue.pack(side='top')
        row=0
        c=0
        for key in self.productDict:
                
            catBox = Frame(catalogue)
            catBox.grid(row=row, column=c)
            if int(key):
                instock = 'In Stock'
            else:
                instock = 'Out of Stock'
                
            thumbimg = PhotoImage(file=self.productDict[key].thumb).subsample(100,100)
            productdetails = '{name}\nPKR {price}\n{instock}'.format(name=self.productDict[key].product_name,price=self.productDict[key].unit_price, instock = instock) 
            Button(catBox, image=thumbimg,compound='center', text=productdetails, command= lambda: self.addItem(key)).pack()
            row+=1


class DisplayCart(Frame, GUIRouter):

    def __init__(self,r,controller):

        Frame.__init__(self,r)
        cart = self.frames[customerScreen]
        columns = ['product_name', 'product_id', 'unit_price']
        c = 0
        for title in columns:
            Label(self, text=title).grid(row=0,column=c)
            c+=1
        Label(self, text='Units Bought').grid(row=0,column=c)
        Label(self, text='').grid(row=0, column=c+1)
        row=0
        for item in cart.item_dict:
            if cart.item_dict[item]:            # if units bought > 0
                
                img = PhotoImage(file=cart.productDict[item].thumb).subsample(100,100)
                f = Label(self, image=img)
                f.image=img
                f.grid(row=row,column=0)
                
                c=1
                for field in columns:
                    Label(self, text=getattr(cart.productDict[item],field)).grid(row=row,column=c)
                    c+=1
                Label(self,text=cart.item_dict[item]).grid(row=row,column=c)
                Button(self, text='Remove', command=cart.delItem(item)).grid(row=row,column=c+1)
                row+=1
        Label(self, text='Total Amount :').grid(row=row, column=2)
        cart.calcCartBill()
        Label(self,text=cart.cart_bill).grid(row=row, column=3)
        Button(self, text='Return to Shop',command=lambda:controller.show_frame(customerScreen)).grid(row=row+1,column=2)

a = GUIRouter()
a.mainloop()
        



    


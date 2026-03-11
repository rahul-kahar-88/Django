from django.shortcuts import render ,redirect
from app.models import *
from django.contrib import messages
from django.core.mail import send_mail



# Create your views here.

def index(req):
    return render(req,'index.html')

def Registration(req):
    if req.method == 'POST':
        n=req.POST.get('name')
        e=req.POST.get('email')
        c=req.POST.get('contact')
        p=req.POST.get('password')
        cp=req.POST.get('cpassword')
        ph=req.FILES.get('photo')
        a=req.FILES.get('audio')
        v=req.FILES.get('video')
        d=req.FILES.get('resume')
        q=req.POST.getlist('qualification')
        g=req.POST.get('gender')
        ch=req.POST.get('city')
        user = Employee.objects.filter(Email=e)
        print(user)
        if not user:
            if p == cp:
                Employee.objects.create(
                    Name=n,
                    Email=e,
                    Contact=c,
                    Password=p,
                    CPassword=cp,
                    Photo=ph,
                    Audio=a,
                    Video=v,
                    Resume=d,
                    City=ch,
                    Qualification=q,
                    Gender=g
                )
                return redirect('Login')
            else:
                msg = "Password and confirm not matched"
                userdata = {'name':n,'contact':c,'email':e}
                return render(req,'Registration.html',{'pmsg':msg,'data':userdata})
        
        else:
            msg='This email already exist'
            return render(req,'Registration.html',{'msg':msg})
    
    return render(req,'Registration.html')

# def Login(req):
#     if req.method=='POST':
#         e=req.POST.get('email')
#         p=req.POST.get('password')
#         if e=='admin@gmail.com' and p=='admin':
#             a_data = {
#                 'id':1,
#                 'name':'Admin',
#                 'email':'admin@gmail.com',
#                 'password':'admin',
#                 'image':'images/admin.png'
#             }
#             req.session['a_data']=a_data
#             return redirect('admindashboard')
            
#         else:
#             user=Employee.objects.filter(Email=e)
#             if not user:
#                 msg="Register First"
#                 return redirect('Registration')
#             else:
#                 userdata = Employee.objects.get(Email=e)
#                 if p==userdata.Password:
#                     req.session['user_id']=userdata.id 
#                     return redirect('userdeshboard')
#                 else:
#                     msg='Email & password not match'
#                     return render(req, 'Login.html',{'x':msg})
            
#     return render(req,'Login.html')


def Login(req):
    if req.method=='POST':
        e=req.POST.get('email')
        p=req.POST.get('password')
        if e=='admin@gmail.com' and p=='admin':
            a_data = {
                'id':1,
                'name':'Admin',
                'email':'admin@gmail.com',
                'password':'admin',
                'image':'images/admin.png'
            }
            req.session['a_data']=a_data
            return redirect('admindashboard')
            
        else:
            employee=Add_Employee.objects.filter(Email=e)
            if employee:
                emp_data= Add_Employee.objects.get(Email=e)
                if p==emp_data.Code:
                   req.session['emp_id']= emp_data.id
                   return redirect('empdashboard')
                else:
                   messages.warning(req,'Email and password not match')
                   return redirect('Login') 
            else:
                messages.warning(req,'you are not my employees')
                return redirect('Login')
            
    return render(req,'Login.html')

def empdashboard(req):
    if 'emp_id' in req.session:
        eid = req.session.get('emp_id')
        emp_data=Add_Employee.objects.get(id=eid)
        return render(req,'empdashboard.html',{'data':emp_data})

    else:
        return redirect('Login')
    

def userdeshboard(req):
    if 'user_id' in req.session:
        x=req.session.get('user_id')
        userdata = Employee.objects.get(id=x)
        return render(req, 'userdeshboard.html',{'data':userdata})
    return render('Login')

def admindashboard(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        return render(req,'admindashboard.html',{'data':a_data})
    else:
        return redirect('Login')
    




def logout(req):
    if 'user_id' in req.session:
        req.session.flush()
        return redirect('Login')
    elif 'a_data' in req.session:
        req.session.flush()
        return redirect('Login')
    else:
        return redirect('Login')


def add_dep(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
    else:
        return redirect('Login')
    
def save_dep(req):
    if 'a_data' in req.session:
        if req.method == 'POST':
           
            dn=req.POST.get('dep_name')
            dd=req.POST.get('dep_desc')
            dh=req.POST.get('dep_head')
            dept=Department.objects.filter(dep_name=dn)
            if dept:
               messages.warning(req,'department already exist')
               a_data= req.session.get('a_data')
               return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
            else:
                Department.objects.create(dep_name=dn,dep_desc=dd,dep_head=dh)
                messages.success(req,'Department created')
                a_data= req.session.get('a_data')
                return render(req,'admindashboard.html',{'data':a_data , 'add_dep':True})
    else:
        return redirect('Login')
    
def show_dep(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        departments = Department.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'show_dep':True, 'departments':departments})
    else:
        return redirect('Login')
    

def add_emp(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        departments = Department.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'add_emp':True,'departments':departments})
    else:
        return redirect('Login')
    

def save_emp(req):
    if 'a_data' in req.session:
        if req.method == 'POST':
           
            en=req.POST.get('name')
            ee=req.POST.get('email')    
            ec=req.POST.get('contact')
            ed=req.POST.get('dept')
            ei=req.FILES.get('image')
            eco=req.POST.get('code')
            send_mail(
                 "mail from MyApp",
                 f'this is information regarding your company exdential : name={en}, \n email={ee}, \n contact={ec}, \n dept={ed} ,\n code={eco} , \nimage={ei} ',
                 "rahulkahar88588@gmail.com",
                 [ee],
                 fail_silently=False,
            )

            emp=Add_Employee.objects.filter(Email=ee)
            if emp:
                messages.warning(req,'Employee already exist')
                a_data = req.session.get('a_data')
                departments = Add_Employee.objects.all()
                return render(req,'admindashboard.html',{'data':a_data , 'add_emp':True,'departments':departments})
            else:
                Add_Employee.objects.create(Name=en,Email=ee,Contact=ec,Dept=ed,Image=ei,Code=eco)
                messages.success(req,'Employee created')
                a_data= req.session.get('a_data')
                departments = Add_Employee.objects.all()
                return render(req,'admindashboard.html',{'data':a_data , 'add_emp':True,'departments':departments})
    else:
        return redirect('Login')
    

def show_emp(req):
     if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        departments = Add_Employee.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'show_emp':True, 'departments':departments})
     else:
        return redirect('Login')
     
def emp_all_query(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        empallquery = Query.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'emp_all_query':True, 'all_query':empallquery})
    else:
        return redirect('Login')
    
def reply(req , pk):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        q_data=Query.objects.get(id=pk)
        emp_all_query=Query.objects.all()
        return render(req, 'admindashboard.html', {'data':a_data , 'q_data':q_data , 'emp_all_query':emp_all_query} )

def a_reply(req , pk):
    if 'a_data' in req.session:
        q_old_data= Query.objects.get(id=pk)
        if req.method == 'POST':
            ar=req.POST.get('reply')
            q_old_data.Reply=ar
            q_old_data.Status="done"
            q_old_data.save()
        a_data = req.session.get('a_data')
        emp_all_query=Query.objects.all()
        return render(req, 'admindashboard.html', {'a_data':a_data  , 'emp_all_query':emp_all_query} )
    
def add_item(req):
    if 'a_data' in req.session:
        a_data=req.session.get('a_data')
        if req.method == "POST":
            name = req.POST.get('item_name')
            desc = req.POST.get('item_desc')
            price = req.POST.get('item_price')
            color = req.POST.get('item_color')
            category = req.POST.get('item_category')
            quantity = req.POST.get('item_quantity')
            image = req.FILES.get('item_image')

            Item.objects.create(
                item_name=name,
                item_desc=desc,
                item_price=price,
                item_color=color,
                item_category=category,
                item_quantity=quantity,
                item_image=image
            )
            return redirect('admindashboard')
        else:
            a_data=req.session.get('a_data')
            return render(req,'admindashboard.html',{'data':a_data , 'add_item':True})  
    else: 
        return redirect('Login') 

def show_item(req):
    if 'a_data' in req.session:
        a_data=req.session.get('a_data')
        all_items = Item.objects.all()
        return render(req,'admindashboard.html',{'data':a_data , 'show_item':True , 'all_items':all_items})
    else:
        return redirect('Login')
  



# def profile(req):
#     if 'a_data' in req.session:
#         a_data = req.session.get('a_data')
#         return render(req,'empdashboard.html',{'data':a_data , 'profile':True})
#     else:
#         return redirect('empdashboard')


# def Show_profile(req):
#     if 'a_data' in req.session:
#         a_data = req.session.get('a_data')
#         profile = Add_Employee.objects.all()
#         return render(req,'empdashboard.html',{'data':a_data , 'show_profile':True,  'profile':profile})
#     else:
#         return redirect('empdashboard')
  

def profile(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Add_Employee.objects.get(id=eid)
      return render(req,'empdashboard.html',{'data':emp_data , 'profile':True})
   return redirect('Login')
  

def setting(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Add_Employee.objects.get(id=eid)
      return render(req,'empdashboard.html',{'data':emp_data , 'setting':True})
   return redirect('Login')

def query(req):
   if 'emp_id' in req.session:
      eid = req.session.get('emp_id')
      emp_data = Add_Employee.objects.get(id=eid)
      departments = Department.objects.all()
      return render(req,'empdashboard.html',{'data':emp_data , 'query':True ,'emp_dept':departments })
   else:
      return redirect('Login')
  
def querydata(req):
    if 'emp_id' in req.session:
      if req.method == 'POST':
         n=req.POST.get('name')
         e=req.POST.get('email')
         d=req.POST.get('department')
         q=req.POST.get('query')
         Query.objects.create(Name=n,Email=e,Dept=d,Query=q)
         messages.success(req,'Query submitted')
         eid = req.session.get('emp_id')
         emp_data = Add_Employee.objects.get(id=eid)
         departments = Department.objects.all()
         return render(req,'empdashboard.html',{'data':emp_data , 'query':True ,'emp_dept':departments })
    else:
        return redirect('Login')


def allquery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        all_query = Query.objects.filter(Email=emp_data.Email)
        return render(req, 'empdashboard.html', {'data':emp_data,'allquery':True , 'all_query':all_query})
    else:
        return redirect('Login')
    

def pendingquery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        all_query = Query.objects.filter(Email=emp_data.Email, Status="pending")
        return render(req, 'empdashboard.html', {'data':emp_data,'pendingquery':True , 'all_query':all_query})
    else:
        return redirect('Login')
    
def donequery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        all_query = Query.objects.filter(Email=emp_data.Email, Status="done")
        return render(req, 'empdashboard.html', {'data':emp_data,'donequery':True , 'all_query':all_query})
    else:
        return redirect('Login')


def edit_all_query(req, pk):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        old_querydata = Query.objects.get(id=pk)
        emp_dept = Department.objects.all()
        all_query = Query.objects.filter(Email=emp_data.Email)
        return render(req, 'empdashboard.html', { 'data': emp_data, 'allquery': True, 'old_querydata': old_querydata, 'emp_dept': emp_dept, 'all_query': all_query})
    else:
        return redirect('Login')

def updated_query(req, pk):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        if req.method == 'POST':
            d = req.POST.get('department')
            q = req.POST.get('query')
            old_q_data = Query.objects.get(id=pk)
            old_q_data.Dept = d
            old_q_data.Query = q
            old_q_data.save()
            messages.success(req, "Query updated successfully")
            emp_data = Add_Employee.objects.get(id=e_id)
            all_query = Query.objects.filter(Email=emp_data.Email)
            return render(req, 'empdashboard.html', { 'data': emp_data, 'allquery': True, 'all_query': all_query})
    else:
        return redirect('Login')
    
    
    



# def emp_q_delete(req, id):
#     if 'emp_id' in req.session:
#         e_id = req.session.get('emp_id')
#         emp_data = AddEmployee.objects.get(id=e_id)
#         check_query = Query.objects.get(id=id)
#         check_query.delete()
#         all_query = Query.objects.filter(Email=emp_data.Email)
#         messages.success(req, 'Query deleted')
#         return render(req, 'empdeshbord.html', { 'data': emp_data, 'allquery': True, 'all_query': all_query
#         })
#     else:
#         return redirect('Login')


def emp_q_delete(req, id):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        q = Query.objects.filter(id=id).first()
        if q:
            q.delete()
            messages.success(req, "Query deleted successfully")
        else:
            messages.warning(req, "Query already deleted")
        return redirect('empdashboard')

    else:
        return redirect('Login')




from django.db.models import Q 

def search(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Add_Employee.objects.get(id=e_id)
        if req.method == 'POST':
          s=req.POST.get('search')

        #   all_query = Query.objects.filter(Email=emp_data.Email,Query=s)
        #   all_query = Query.objects.filter(Email__icontains=emp_data.Email,Query__icontains=s)
        #   all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains=s)
        #   all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains=s , Dept__icontains=s)
        #   all_query = Query.objects.filter(Email=emp_data.Email and (Q(Query__icontains=s) | Q(Dept__icontains=s)))
          all_query = Query.objects.filter(Email=emp_data.Email).filter(Q(Query__icontains=s) | Q(Dept__icontains=s))
          return render(req, 'empdashboard.html', {'data':emp_data, 'allquery':True , 'all_query':all_query ,'s':s})
    else:
        return redirect('Login')
   
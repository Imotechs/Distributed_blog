from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm
from django.views.generic import(
    ListView,DeleteView,DetailView,CreateView,UpdateView
)
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post

class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'home.html'
    context_object_name = 'posts'
    #cutting down many post appearance on a single screen to 4
    paginate_by = 4

class PostDetail(DetailView):
    model = Post
    template_name = 'detail.html'


def search(request):
    search_items = request.GET['item']
    search_result = Post.objects.filter(Q(title__icontains = search_items)).filter(status = 1)
    context = {
        'searched_posts':search_result
    }
    return render(request,'search.html',context)



def register(request,*args,**kwargs):
    if request.method =="POST":
        #we shall authenticate with email OR username, so make sure emails are unique on registration
        if User.objects.filter(email = request.POST['email']):
            context = {
                {"msg":"Email already registered!"},
            }
            return render(request,'register.html',context)
        else:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
            
            else:
                #form is not valid so user refill the form
                context = {
                    'messages':form.errors,
                        }
                return render(request,'register.html',context)
    
    return render(request,'register.html')


#login View
def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        #try authenticating with provided credentials
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                #user found and active?, Log user in
                auth_login(request,user)
                messages.info(request,'Great to have you back!')
                return redirect('home')
            else:
                context = {'msg':'This Account is inactive!'}
                return render(request,'login.html', {'msg':context})
        elif user is None:
            #user not found redirect back with message
            context = {'msg':'No account with matching Credentials!'}
            return render(request,'login.html', context)

    return render(request,'login.html')



class CreatePostView(LoginRequiredMixin,CreateView):
    template_name = 'add_post.html'
    model = Post
    fields = ['title','content','cover','status']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
createpost = CreatePostView.as_view()

class UpdatePostView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    template_name = 'edit_post.html'
    model = Post
    fields = ['title','content','cover','status']
    #lets check who is trying to edit the post and give access if its the owner or an admin
    def test_func(self,*args,**kwargs):
        post = self.get_object()
        if post.author == self.request.user or self.request.user.is_superuser:
             return True
        return False  
update_post = UpdatePostView.as_view()

class DeletePostView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    template_name = 'delete_post.html'
    model = Post
    success_url = '/'
    def test_func(self,*args,**kwargs):
        post = self.get_object()
        if post.author == self.request.user or self.request.user.is_superuser:
             return True
        return False  
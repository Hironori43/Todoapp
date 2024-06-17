from django.shortcuts import render 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# ユーザーがログインしていることを確認。ログインしていないユーザーがToDoリストにアクセスしようとすると、ログインページにリダイレクトされる。
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Todo


class TodoList(LoginRequiredMixin, ListView):
    # このビューで作成するモデルの指定
    model = Todo
    # テンプレート内では、ToDoリストがtasksという名前で利用可能
    context_object_name = "tasks"
    
    def get_queryset(self):
        # ソート順を取得、デフォルトは締め切り昇順
        sort_order = self.request.GET.get('sort', 'deadline_asc')
        if sort_order == 'deadline_desc':
            return Todo.objects.filter(user=self.request.user).order_by('-deadline')
        return Todo.objects.filter(user=self.request.user).order_by('deadline')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'deadline_asc')
        return context
    
class TodoDetail(DetailView):
        model = Todo
        # テンプレート内では、ToDoリストがtaskという名前で利用可能
        context_object_name = "task"
        
class TodoCreate(LoginRequiredMixin, CreateView):
    model = Todo
    # ユーザーに入力させるフィールド指定
    fields = ['title', 'description', 'deadline']
    # Todoが正常に作成された後Listにリダイレクト
    success_url = reverse_lazy('list')
    # ビューで使うテンプレートの名前指定
    template_name = 'todo/todo_form.html'

    def form_valid(self, form):
        # 現在ログインしているユーザーの情報設定
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # context_dataメソッドの結果をcontextに格納
        context = super().get_context_data(**kwargs)
        # actionキーにcreateを割り当て
        context['action'] = 'create'
        return context
    
class TodoUpdate(UpdateView):
    model = Todo
    fields = ['title', 'description', 'deadline']
    success_url = reverse_lazy('list')
    template_name = 'todo/todo_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # actionキーにupdateを割り当て
        context['action'] = 'update'
        # ビューで更新されるTodoインスタンスの取得、ここで現在のTodoを渡す
        context['task'] = self.get_object() 
        return context
    
class TodoDelete(DeleteView):
    model = Todo
    context_object_name = "task"
    success_url = reverse_lazy("list")
    

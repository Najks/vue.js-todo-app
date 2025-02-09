import { createRouter, createWebHistory } from "vue-router";
import RegisterView from "../views/RegisterView.vue";
import LoginView from "../views/LoginView.vue";
import DashboardView from "../views/DashboardView.vue";
import HomeView from "@/views/HomeView.vue";
import CreateView from "@/views/CreateTaskView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/register", component: RegisterView },
  { path: "/login", component: LoginView },
  { path: "/dashboard", component: DashboardView },
  {path: "/create", component: CreateView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

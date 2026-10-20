import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
    history: createWebHistory(),

    routes: [
        {
            path:"/",
            name:"home",
            component: HomeView
        },
        {
            path:"/about",
            name:"about",
            component: AboutView
        },
        //dynamic router
        {
            path: "/users/:id",
            name: "user",
            component: () => import("../views/UserView.vue")
        }
    ]
})

export default router
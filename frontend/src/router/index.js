import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import AboutView from '../views/aboutView.vue'
import { Component } from 'react'

const router = createRouter({
    history: createWebHistory(),

    router: [
        {
            path:"/",
            name:"home",
            Component: HomeView
        },
        {
            path:"/about",
            name:"about",
            Component: AboutView
        },
        //dynamic router
        {
            path: "/users/:id",
            name: "user",
            Component: () => import("../views/UserView.vue")
        }
    ]
})

export default router
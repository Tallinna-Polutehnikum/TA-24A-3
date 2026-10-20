import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import MovieScheduleView from '../views/MovieScheduleView.vue'
import MoviesView from '../views/MoviesView.vue'
import UserView from '../views/UserView.vue'
import CinemasView from '../views/CinemasView.vue'
import GenresView from '../views/GenresView.vue'
import BookingView from '../views/BookingView.vue'

const router = createRouter({
    history: createWebHistory(),

    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/KinoKava',
            name: 'MovieSchedule',
            component: MovieScheduleView
        },
        {
            path: '/filmid',
            name: 'Movies',
            component: MoviesView
        },
        {
            path: '/users/:id',
            name: 'user',
            component: UserView
        },
        {
            path: '/kinod',
            name: 'Cinemas',
            component: CinemasView
        },
        {
            path: '/kasutaja',
            name: 'User',
            component: UserView
        },
        {
            path: '/zanrid',
            name: 'Genres',
            component: GenresView
        },
        {
            path: '/broneerimine',
            name: 'Booking',
            component: BookingView
        }
    ]
})

export default router

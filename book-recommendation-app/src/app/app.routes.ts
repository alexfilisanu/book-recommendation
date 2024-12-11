import {Routes} from '@angular/router';
import {AdminLayoutComponent} from "./admin-layout/admin-layout.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {BooksComponent} from "./books/books.component";
import {BookComponent} from "./book/book.component";
import {BookRecommendationsComponent} from "./book-recommendations/book-recommendations.component";
import {LoginComponent} from "./login/login.component";
import {RegisterComponent} from "./register/register.component";
import {NotFoundComponent} from "./not-found/not-found.component";

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: '',
    component: AdminLayoutComponent,
    children: [
      {
        path: 'dashboard',
        component: DashboardComponent
      },
      {
        path: 'books',
        component: BooksComponent
      },
      {
        path: 'book/:isbn',
        component: BookComponent
      },
      {
        path: 'book/recommendations/:isbn',
        component: BookRecommendationsComponent
      }
    ]
  },
  {
    path: '**',
    component: NotFoundComponent
  }
];

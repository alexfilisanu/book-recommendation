import {Routes} from '@angular/router';
import {AdminLayoutComponent} from "./components/admin-layout/admin-layout.component";
import {DashboardComponent} from "./pages/dashboard/dashboard.component";
import {BooksComponent} from "./pages/book-pages/books/books.component";
import {BookComponent} from "./pages/book-pages/book/book.component";
import {BookRecommendationsComponent} from "./pages/book-pages/book-recommendations/book-recommendations.component";
import {LoginComponent} from "./pages/auth/login/login.component";
import {RegisterComponent} from "./pages/auth/register/register.component";
import {NotFoundComponent} from "./pages/not-found/not-found.component";
import {MyReviewsComponent} from "./pages/my-reviews/my-reviews.component";

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
      },
      {
        path: 'my-reviews',
        component: MyReviewsComponent
      }
    ]
  },
  {
    path: '**',
    component: NotFoundComponent
  }
];

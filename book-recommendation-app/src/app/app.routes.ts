import {Routes} from '@angular/router';
import {AdminLayoutComponent} from "./admin-layout/admin-layout.component";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {BooksComponent} from "./books/books.component";
import {BookComponent} from "./book/book.component";

export const routes: Routes = [
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
      }
    ]
  }
];

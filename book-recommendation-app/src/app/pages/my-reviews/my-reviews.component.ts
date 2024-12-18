import {Component} from '@angular/core';

@Component({
  selector: 'app-my-reviews',
  imports: [],
  templateUrl: './my-reviews.component.html',
  standalone: true,
  styleUrl: './my-reviews.component.css'
})
export class MyReviewsComponent {

  public userName: string | null = sessionStorage.getItem('username');
}

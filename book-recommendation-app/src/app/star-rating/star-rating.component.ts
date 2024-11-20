import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-star-rating',
  standalone: true,
  imports: [],
  templateUrl: './star-rating.component.html',
  styleUrl: './star-rating.component.css'
})
export class StarRatingComponent {
  @Input() rating: number = 0;

  public stars() {
    return Array.from({length: 5}, (_, index) => {
      const starRating = this.rating - index;
      if (starRating >= 1) return 'full';
      if (starRating >= 0.5) return 'half';
      return 'empty';
    });
  }
}

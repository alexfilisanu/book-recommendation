import { Component } from '@angular/core';
import { BookRecommendationsService } from './book-recommendations.service';
import {ActivatedRoute, Router} from "@angular/router";
import {StarRatingComponent} from "../star-rating/star-rating.component";

@Component({
  selector: 'app-book-recommendations',
  standalone: true,
  imports: [
    StarRatingComponent
  ],
  templateUrl: './book-recommendations.component.html',
  styleUrl: './book-recommendations.component.css'
})
export class BookRecommendationsComponent {

  public recommendations: any[] = [];

  constructor(private route: ActivatedRoute, private bookRecommendationsService: BookRecommendationsService, private router: Router) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const {isbn} = params;
      this.getBooks(isbn);
    })
  }

  private getBooks(isbn: string): void {
    this.bookRecommendationsService.getBookRecommendation(isbn).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations;
      },
      error: (error) => {
        console.error('Error fetching book recommendations', error);
      }
    });
  }

  public getRating(ratingStr: string): number {
    const rating = parseFloat(ratingStr);
    const roundedRating = Math.round(rating);
    return roundedRating / 2;
  }

  public viewBookDetails(isbn: string): void {
    this.router.navigate(['/book', isbn])
      .catch(error => console.error('Error navigating to book details:', error));
  }
}

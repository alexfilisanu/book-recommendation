import {Component} from '@angular/core';
import {StarRatingComponent} from "../star-rating/star-rating.component";
import {BookService} from "./book.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-book',
  standalone: true,
  imports: [
    StarRatingComponent
  ],
  templateUrl: './book.component.html',
  styleUrl: './book.component.css'
})
export class BookComponent {

  public book: any = {};

  constructor(private bookService: BookService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const { isbn } = params;
      this.getBook(isbn);
    })
  }

  private getBook(isbn: string): void {
    this.bookService.getBook(isbn).subscribe({
      next: (response) => {
        this.book = response.book;
      },
      error: (error) => {
        console.error(`Error fetching book with ISBN ${isbn}`, error);
      }
    });
  }

  public getRating(ratingStr: string): number {
    const rating = parseFloat(ratingStr);
    const roundedRating = Math.round(rating);
    return roundedRating / 2;
  }
}

import {Component} from '@angular/core';
import {StarRatingComponent} from "../star-rating/star-rating.component";
import {BookService} from "./book.service";
import {ActivatedRoute, Router} from "@angular/router";

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
  public selectedReview: number | null = null;

  constructor(private bookService: BookService, private route: ActivatedRoute, private router: Router) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const {isbn} = params;
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

  public sendReview(): void {
    this.router.navigate([`/book/recommendations/${this.book.ISBN}`], {queryParams: {title: this.book.Book_Title}})
      .catch(error => console.error('Error navigating to book recommendations', error));
  }
}

import {Component} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {BooksService} from './books.service';
import {StarRatingComponent} from "../star-rating/star-rating.component";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-books',
  standalone: true,
  imports: [
    NgForOf,
    NgIf,
    StarRatingComponent
  ],
  templateUrl: './books.component.html',
  styleUrl: './books.component.css'
})
export class BooksComponent {
  public books: any[] = [];
  public currentPage: number = 1;
  public totalBooks: number = 0;
  public totalPages: number = 0;
  private booksPerPage: number = 8;
  private searchQuery: string = '';

  constructor(private booksService: BooksService, private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const { q = '' } = params;
      this.searchQuery = q;
      this.currentPage = 1;
      this.getTotalBooks();
      this.getBooks();
    });
  }

  private getTotalBooks(): void {
    this.booksService.getTotalBooks(this.searchQuery).subscribe({
      next: (response) => {
        this.totalBooks = response.totalBooks;
        this.totalPages = Math.ceil(this.totalBooks / this.booksPerPage);
      },
      error: (error) => {
        console.error('Error fetching total books', error);
      }
    });
  }

  private getBooks(page: number = this.currentPage) {
    this.booksService.getBooks(this.searchQuery, page, this.booksPerPage).subscribe({
      next: (response) => {
        this.books = response.books;
      },
      error: (error) => {
        console.error(`Error fetching books for page ${page}`, error);
      }
    });
  }

  public getRating(ratingStr: string): number {
    const rating = parseFloat(ratingStr);
    const roundedRating = Math.round(rating);
    return roundedRating / 2;
  }

  public nextPage() {
    this.getBooks(++this.currentPage);
  }

  public previousPage() {
    this.getBooks(--this.currentPage);
  }
}

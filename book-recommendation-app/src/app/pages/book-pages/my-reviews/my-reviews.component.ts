import {Component} from '@angular/core';
import {BookService} from "../book.service";
import {ActivatedRoute, Router} from "@angular/router";
import {NgIf} from "@angular/common";
import {BooksPaginationComponent} from "../../../components/books-pagination/books-pagination.component";

@Component({
  selector: 'app-my-reviews',
  imports: [
    NgIf,
    BooksPaginationComponent
  ],
  templateUrl: './my-reviews.component.html',
  standalone: true,
  styleUrl: './my-reviews.component.css'
})
export class MyReviewsComponent {

  public userName: string | null = sessionStorage.getItem('username');
  public userId: string | null = sessionStorage.getItem('userId');
  public reviews: any[] = [];
  public currentPage: number = 1;
  public totalReviews: number = 0;
  public totalPages: number = 0;
  private booksPerPage: number = 4;

  constructor(private bookService: BookService, private route: ActivatedRoute, private router: Router) {
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(() => {
      this.currentPage = 1;
      this.getTotalBooks();
      this.getBooks();
    });
  }

  private getTotalBooks(): void {
    if (!this.userId) {
      console.error('User ID is not available');
      return;
    }

    this.bookService.getMyTotalReviews(this.userId).subscribe({
      next: (response) => {
        this.totalReviews = response.totalReviews;
        this.totalPages = Math.ceil(this.totalReviews / this.booksPerPage);
      },
      error: (error) => {
        console.error('Error fetching my total reviews', error);
      }
    });
  }

  private getBooks(page: number = this.currentPage): void {
    if (!this.userId) {
      console.error('User ID is not available');
      return;
    }

    this.bookService.getMyReviews(this.userId, page, this.booksPerPage).subscribe({
      next: (response) => {
        this.reviews = response.reviews;
      },
      error: (error) => {
        console.error(`Error fetching books for page ${page}`, error);
      }
    });
  }

  public onPageChange(newPage: number): void {
    this.currentPage = newPage;
    this.getBooks();
  }

  public getPersonalizedRecommendations(): void {
   this.router.navigate([`/user/recommendations/${this.userId}`])
     .catch(error => console.error('Error navigating to personalized recommendations', error));
  }
}

import {Component} from '@angular/core';
import {BooksPaginationComponent} from "../../../components/books-pagination/books-pagination.component";
import {ActivatedRoute} from "@angular/router";
import {BookService} from "../book.service";

@Component({
  selector: 'app-personalized-recommendations',
  imports: [
    BooksPaginationComponent
  ],
  templateUrl: './personalized-recommendations.component.html',
  styleUrl: './personalized-recommendations.component.css'
})
export class PersonalizedRecommendationsComponent {

  public recommendations: any[] = [];
  public displayedRecommendations: any[] = [];
  public currentPage: number = 1;
  public totalBooks: number = 0;
  public totalPages: number = 0;
  private booksPerPage: number = 8;

  constructor(private route: ActivatedRoute, private bookService: BookService) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const {userId} = params;
      this.route.queryParams.subscribe(() => {
        this.currentPage = 1;
        this.getTotalBooks(userId);
      });
    });
  }

  private getTotalBooks(userId: string): void {
    this.bookService.getUserRecommendation(userId).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations;
        this.totalBooks = this.recommendations.length;
        this.totalPages = Math.ceil(this.totalBooks / this.booksPerPage);
        this.getBooks();
      },
      error: (error) => {
        console.error('Error fetching book recommendations', error);
      }
    });
  }

  private getBooks(page: number = this.currentPage): void {
    const start = (page - 1) * this.booksPerPage;
    const end = start + this.booksPerPage;
    this.displayedRecommendations = this.recommendations.slice(start, end);
  }

  public onPageChange(newPage: number): void {
    this.currentPage = newPage;
    this.getBooks();
  }
}

import {Component} from '@angular/core';
import {BookService} from '../book.service';
import {ActivatedRoute} from "@angular/router";
import {BooksPaginationComponent} from "../../../components/books-pagination/books-pagination.component";

@Component({
  selector: 'app-book-recommendations',
  standalone: true,
  imports: [
    BooksPaginationComponent
  ],
  templateUrl: './book-recommendations.component.html',
  styleUrl: './book-recommendations.component.css'
})
export class BookRecommendationsComponent {

  public recommendations: any[] = [];
  public displayedRecommendations: any[] = [];
  public bookTitle: string = '';
  public currentPage: number = 1;
  public totalBooks: number = 0;
  public totalPages: number = 0;
  private booksPerPage: number = 4;

  constructor(private route: ActivatedRoute, private bookService: BookService) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const {isbn} = params;
      this.route.queryParams.subscribe(queryParams => {
        const {title} = queryParams;
        this.bookTitle = title;
        this.currentPage = 1;
        this.getTotalBooks(isbn);
      });
    });
  }

  private getTotalBooks(isbn: string): void {
    this.bookService.getBookRecommendation(isbn).subscribe({
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

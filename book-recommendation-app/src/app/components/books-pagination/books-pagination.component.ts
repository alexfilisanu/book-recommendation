import {Component, Input, Output} from '@angular/core';
import {EventEmitter} from '@angular/core';
import {BookPreviewComponent} from "../book-preview/book-preview.component";

@Component({
  selector: 'app-books-pagination',
  imports: [
    BookPreviewComponent
  ],
  templateUrl: './books-pagination.component.html',
  styleUrl: './books-pagination.component.css'
})
export class BooksPaginationComponent {

  @Input() books: any[] = [];
  @Input() currentPage: number = 1;
  @Input() totalPages: number = 1;

  @Output() pageChange: EventEmitter<number> = new EventEmitter<number>();

  public previousPage(): void {
    this.pageChange.emit(this.currentPage - 1);
  }

  public nextPage(): void {
    this.pageChange.emit(this.currentPage + 1);
  }
}

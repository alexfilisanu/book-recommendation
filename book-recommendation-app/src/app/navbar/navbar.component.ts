import {Component} from '@angular/core';
import {Router} from "@angular/router";
import {BooksService} from "../books/books.service";
import {FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  public searchBooksFormGroup!: FormGroup;
  public searchQuery: string = '';

  constructor(private booksService: BooksService, private router: Router, private formBuilder: FormBuilder) {}

  ngOnInit(): void {
    this.searchBooksFormGroup = this.formBuilder.group({
      searchQuery: new FormControl('')
    });
  }

  public searchBooks(): void {
    this.searchQuery = this.searchBooksFormGroup.get('searchQuery')?.value;

    if (this.searchQuery.trim()) {
      this.booksService.getBooks(this.searchQuery).subscribe({
        next: (response) => {
          console.log('Search results:', response.books);
          // Pass data to BooksComponent or handle state management
          this.router.navigate(['/books'], {queryParams: {q: this.searchQuery}})
            .catch(error => console.error('Error navigating to books:', error));
        },
        error: (error) => {
          console.error('Search error:', error);
        }
      });
    }
  }
}

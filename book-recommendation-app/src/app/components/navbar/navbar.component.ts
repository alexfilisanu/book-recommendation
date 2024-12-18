import {Component} from '@angular/core';
import {Router} from "@angular/router";
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

  constructor(private router: Router, private formBuilder: FormBuilder) {
  }

  ngOnInit(): void {
    this.searchBooksFormGroup = this.formBuilder.group({
      searchQuery: new FormControl('')
    });
  }

  public searchBooks(): void {
    this.searchQuery = this.searchBooksFormGroup.get('searchQuery')?.value;

    if (this.searchQuery.trim()) {
      this.router.navigate(['/books'], {queryParams: {q: this.searchQuery}})
        .catch(error => console.error('Error navigating to books:', error));
    }
  }

  public logout(): void {
    sessionStorage.clear();
    this.navigatePage('login');
  }

  public navigatePage(page: string): void {
    this.router.navigate([`/${page}`])
      .catch(error => console.error(`Error navigating to ${page}:`, error));
  }
}

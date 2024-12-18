import {Component} from '@angular/core';
import {AbstractControl, FormBuilder, ReactiveFormsModule, ValidationErrors, Validators} from "@angular/forms";
import {NgClass} from "@angular/common";
import {Router} from "@angular/router";
import {AuthService} from "../auth.service";

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgClass
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

  public isPasswordVisible: boolean = false;
  public isConfirmPasswordVisible: boolean = false;
  public errorMessage: string = '';
  public registerFormGroup: any;

  constructor(private formBuilder: FormBuilder, private authService: AuthService, private router: Router) {
  }

  ngOnInit(): void {
    this.registerFormGroup = this.formBuilder.group({
      username: ['', Validators.required],
      location: ['', Validators.required],
      age: ['', [Validators.required, Validators.min(14)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required, Validators.minLength(6), this.matchPassword.bind(this)]]
    });
  }

  private matchPassword(control: AbstractControl): ValidationErrors | null {
    const password = control.parent?.get("password")?.value;
    const confirmPassword = control.value;

    return password === confirmPassword ? null : {mismatch: true};
  }

  public togglePassword(): void {
    this.isPasswordVisible = !this.isPasswordVisible;
  }

  public toggleConfirmPassword(): void {
    this.isConfirmPasswordVisible = !this.isConfirmPasswordVisible;
  }

  public onSubmit(): void {
    if (this.registerFormGroup?.valid) {
      this.errorMessage = '';

      this.authService.registerUser(this.registerFormGroup.value).subscribe({
        next: (response) => {
          sessionStorage.setItem('isAuthenticated', 'true');
          sessionStorage.setItem('username', response.username);
          this.router.navigate(['/dashboard']).catch(error => {
            console.error('Error navigating to dashboard:', error);
          });
        },
        error: (error) => {
          this.errorMessage = error.error;
          console.error('Error occurred while registering the user:', error);
        }
      });
    } else if (this.areAllFieldsCompleted() && this.registerFormGroup?.get("username").invalid) {
      this.errorMessage = 'Username is invalid';
    } else if (this.areAllFieldsCompleted() && this.registerFormGroup?.get("location").invalid) {
      this.errorMessage = 'Location is invalid';
    } else if (this.areAllFieldsCompleted() && this.registerFormGroup?.get("age").invalid) {
      this.errorMessage = 'Age is invalid';
    } else if (this.areAllFieldsCompleted() && this.registerFormGroup?.get("password").invalid) {
      this.errorMessage = 'Password is invalid';
    } else if (this.areAllFieldsCompleted() && this.registerFormGroup?.get("confirmPassword").invalid) {
      this.errorMessage = 'Confirm password is invalid';
    } else {
      this.errorMessage = 'All fields are required';
    }
  }

  private areAllFieldsCompleted(): boolean {
    return this.registerFormGroup?.get("username").value
      && this.registerFormGroup?.get("location").value
      && this.registerFormGroup?.get("age").value
      && this.registerFormGroup?.get("password").value
      && this.registerFormGroup?.get("confirmPassword").value;
  }

  public navigateLogin() {
    this.router.navigate([`/login`])
      .catch(error => console.error(`Error navigating to login:`, error));
  }
}

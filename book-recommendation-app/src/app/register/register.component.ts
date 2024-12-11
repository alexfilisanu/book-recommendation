import {Component} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {NgClass} from "@angular/common";

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
  public registerFormGroup!: FormGroup;

  constructor(private formBuilder: FormBuilder) {
  }

  ngOnInit(): void {
    this.registerFormGroup = this.formBuilder.group({
      username: new FormControl(''),
      password: new FormControl('')
    });
  }

  public togglePassword(): void {
    this.isPasswordVisible = !this.isPasswordVisible;
  }

  public toggleConfirmPassword(): void {
    this.isConfirmPasswordVisible = !this.isConfirmPasswordVisible;
  }

  public register(): void {
    const username = this.registerFormGroup.get('username')?.value;
    const password = this.registerFormGroup.get('password')?.value;

    if (username.trim() && password.trim()) {
      console.log('Logging in with username:', username, 'and password', password)
    } else {
      console.error('Username and password are required');
    }
  }
}

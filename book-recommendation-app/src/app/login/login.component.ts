import {Component} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {NgClass} from "@angular/common";

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule,
    ReactiveFormsModule,
    NgClass
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  public isVisible: boolean = false;
  public loginFormGroup!: FormGroup;

  constructor(private formBuilder: FormBuilder) {
  }

  ngOnInit(): void {
    this.loginFormGroup = this.formBuilder.group({
      username: new FormControl(''),
      password: new FormControl('')
    });
  }

  public togglePassword(): void {
    this.isVisible = !this.isVisible;
  }

  public login(): void {
    const username = this.loginFormGroup.get('username')?.value;
    const password = this.loginFormGroup.get('password')?.value;

    if (username.trim() && password.trim()) {
      console.log('Logging in with username:', username, 'and password' , password)
    } else {
      console.error('Username and password are required');
    }
  }
}

  import 'package:authentication/main.dart';
import 'package:authentication/pages/home_page.dart';
  import 'package:authentication/pages/login_or_register_page.dart';
  import 'package:flutter/material.dart';
  import 'package:firebase_auth/firebase_auth.dart';

  class AuthenticationPage extends StatelessWidget {
    const AuthenticationPage({super.key});

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        body: StreamBuilder<User?>(
          stream: FirebaseAuth.instance.authStateChanges(),
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return const BottomNavBar();
            }
            else {
              return const LoginOrRegisterPage();
            }
          },
        ),
      );
    }
  }
import 'package:authentication/components/settings_component.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';


class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  void signUserOut() async {
    await FirebaseAuth.instance.signOut();
    Get.offAllNamed('/auth');
  }


  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.white,
        body: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 30),
          child: SingleChildScrollView(
            child: Column(
              children: [
                const SizedBox(
                  height: 80,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text('Settings',
                        style: GoogleFonts.poppins(
                            fontSize: 36, fontWeight: FontWeight.bold)),
                  ],
                ),
                const SizedBox(
                  height: 20,
                ),

                // Profile Settings
                const SettingsComponent(
                  title: 'Profile Settings',
                  description: 'Settings regarding your profile',
                  icon: Icons.person,
                ),

                const SizedBox(
                  height: 20,
                ),

                // News Settings
                const SettingsComponent(
                  title: 'News Settings',
                  description: 'Choose your favourite topics',
                  icon: Icons.newspaper,
                ),

                const SizedBox(
                  height: 20,
                ),

                // Notifications
                const SettingsComponent(
                    title: 'Notifications',
                    description: 'When would you like to be notified?',
                    icon: Icons.notifications),

                const SizedBox(
                  height: 20,
                ),

                // Subscriptions
                const SettingsComponent(
                    title: 'Subscriptions',
                    description: 'Currently, you are in Starter Plan',
                    icon: Icons.star),

                const SizedBox(
                  height: 40,
                ),

                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      'Other',
                      style: GoogleFonts.poppins(
                          fontSize: 26, fontWeight: FontWeight.w400),
                    ),
                  ],
                ),

                const SizedBox(
                  height: 20,
                ),

                // Bug Report
                const SettingsComponent(
                    title: 'Bug Report',
                    description: 'Report bugs easily',
                    icon: Icons.bug_report),

                const SizedBox(
                  height: 20,
                ),

                // Share the App
                const SettingsComponent(
                    title: 'Share the App',
                    description: 'Share on social media networks',
                    icon: Icons.share),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

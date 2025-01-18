import '../components/custom_box_image.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9F9FC),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 30),
            child: Column(
              children: [
                const SizedBox(
                  height: 30,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Image.asset(
                      'assets/images/home_app_logo.png',
                      width: 80,
                    ),
                  ],
                ),
                Text(
                  'Smart Home App',
                  style: GoogleFonts.poppins(
                      fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const SizedBox(
                  height: 20,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Smart homes,\nsmarter living.',
                      style: GoogleFonts.poppins(
                          fontSize: 45,
                          fontWeight: FontWeight.bold,
                          height: 1.2),
                    )
                  ],
                ),
                const SizedBox(
                  height: 30,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(16.0),
                      child: Image.asset(
                        'assets/images/about2.jpg',
                        width: 350,
                      ),
                    ),
                  ],
                ),
                const SizedBox(
                  height: 20,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Flexible(
                      child: Text(
                        'The Smart Home app makes it easier to control all your smart home accessories.',
                        style: GoogleFonts.poppins(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: const Color(0xFF6E6E73)),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ],
                ),
                const SizedBox(
                  height: 30,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      'Smart Features:',
                      style: GoogleFonts.poppins(
                          fontSize: 30, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(
                  height: 15,
                ),
                const CustomBoxImage(
                  itemName: 'Smart Light',
                  itemDescription: 'Nanoleaf A19 Bulb',
                  itemImage: 'assets/images/smart-light.jpg',
                  itemShopDescription: 'Shop Lights & Bulbs >',
                ),
                const SizedBox(
                  height: 15,
                ),
                const CustomBoxImage(
                  itemName: 'Smart AC',
                  itemDescription: 'Air Conditioner',
                  itemImage: 'assets/images/smart-ac.jpg',
                  itemShopDescription: 'Shop ACs >',
                ),
                const SizedBox(
                  height: 20,
                ),
                const CustomBoxImage(
                  itemName: 'Smart Fan',
                  itemDescription: 'Air Circulator Fan',
                  itemImage: 'assets/images/smart-fan.jpeg',
                  itemShopDescription: 'Shop Fans >',
                ),
                const SizedBox(
                  height: 20,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

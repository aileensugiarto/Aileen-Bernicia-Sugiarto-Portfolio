import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CustomBoxImage extends StatelessWidget {
  final String itemName;
  final String itemDescription;
  final String itemImage;
  final String itemShopDescription;

  const CustomBoxImage(
      {super.key,
      required this.itemName,
      required this.itemDescription,
      required this.itemImage,
      required this.itemShopDescription});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 250,
      padding: const EdgeInsets.all(30),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5),
              spreadRadius: 3,
              blurRadius: 10,
            ),
          ]),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            itemName,
            style:
                GoogleFonts.poppins(fontSize: 25, fontWeight: FontWeight.bold),
          ),
          const SizedBox(
            height: 10,
          ),
          Image.asset(
            itemImage,
            fit: BoxFit.cover,
          ),
          const SizedBox(
            height: 10,
          ),
          Text(
            itemDescription,
            style: GoogleFonts.poppins(
                fontSize: 18, color: const Color(0xFF6E6E73),),
          ),
          const SizedBox(
            height: 10,
          ),
          Text(
            itemShopDescription,
            style: GoogleFonts.poppins(fontSize: 16, color: Colors.blue[700], fontWeight: FontWeight.bold),
          )
        ],
      ),
    );
  }
}

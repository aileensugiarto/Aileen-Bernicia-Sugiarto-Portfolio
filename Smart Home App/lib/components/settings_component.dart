import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class SettingsComponent extends StatelessWidget {
  final String title;
  final String description;
  final icon;

  const SettingsComponent({
    super.key,
    required this.title,
    required this.description,
    required this.icon
    });


  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Container(
          width: 56,
          height: 56,
          decoration: BoxDecoration(
            color: Color(0xFF291D31),
            shape: BoxShape.rectangle,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, size: 36, color: Colors.white,),
        ),
        const SizedBox(width: 20),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: GoogleFonts.poppins(
                    fontSize: 17, fontWeight: FontWeight.w500),
              ),
              Text(
                description,
                style: GoogleFonts.poppins(
                    fontSize: 13,
                    fontWeight: FontWeight.w500,
                    color: Colors.grey),
              ),
            ],
          ),
        ),
        InkWell(
          child: Container(
            width: 26,
            height: 26,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(width: 1, color: Colors.grey),
            ),
            child:
                const Icon(Icons.arrow_forward, size: 16, color: Colors.grey),
          ),
        ),
      ],
    );
  }
}

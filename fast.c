#include "perlin/perlin-master/perlin.h"
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdio.h>
// #include <stdio.h>
#define PI 3.141592653589793

int randint(int min, int max) {
    return ((double)rand()/RAND_MAX)*(max-min)+min;
}

typedef struct Colour {
    int a;
    int b;
    int c;
} Colour;

double hueToRgb(double p, double q, double t) {
  if (t < 0) t += 1;
  if (t > 1) t -= 1;
  if (t < 1.0f/6.0f) return p + (q - p) * 6 * t;
  if (t < 1.0f/2.0f) return q;
  if (t < 2.0f/3.0f) return p + (q - p) * (2.0f/3.0f - t) * 6;
  return p;
}

Colour *hslToRgb(double h, double s, double l) {
  double r, g, b;
  h /= 360.0f;
  s /= 100.0f;
  l /= 100.0f;

  printf("%f, %f, %f\n", h, s, l);

  if (s < 0.00001f) {
    r = g = b = l; // achromatic
  } else {
    double q = l < 0.5f ? l * (1 + s) : l + s - l * s;
    double p = 2.0f * l - q;
    r = hueToRgb(p, q, h + 1.0f/3.0f);
    g = hueToRgb(p, q, h);
    b = hueToRgb(p, q, h - 1.0f/3.0f);
  }

  Colour *ret = malloc(sizeof(Colour));
  ret->a = round(r * 255);
  ret->b = round(g * 255);
  ret->c = round(b * 255);
  return ret;
}

int *get_image(int r, int res, int *ret, int seed, int *cols) {
    // int *ret = calloc(sizeof(int), 12*r*r+12*r+3);
    // float *ret = malloc(12*r*r+6*r+3);

    srand(time(NULL));

    Colour *col1 = hslToRgb((double)randint(0, 360), (double)randint(20, 80), (double)randint(10, 80));
    int col_r1 = col1->a;
    int col_g1 = col1->b;
    int col_b1 = col1->c;
    free(col1);

    Colour *col2 = hslToRgb((double)randint(0, 360), (double)randint(20, 80), (double)randint(10, 80));
    int col_r2 = col2->a;
    int col_g2 = col2->b;
    int col_b2 = col2->c;
    free(col2);

    cols[0] = col_r1;
    cols[1] = col_g1;
    cols[2] = col_b1;
    cols[3] = col_r2;
    cols[4] = col_g2;
    cols[5] = col_b2;


    for (int j = 0; j < res; j++) {
        for (int i = 0; i < res; i++) {
            double in = (double)i/(double)res;
            double jn = (double)j/(double)res;
            float noise = pnoise2d(in, jn, 0.8, 6, seed);
            noise = (noise < -1.0f) ? -1.0f : (noise > 1.0f) ? 1.0f : noise;
            int x = round(r*sin(PI*in)*cos(PI*jn) + r);
            int y = round(r*cos(PI*in) + r);
            int c = ((2*r+1)*y + x)*3; 
            // int ci = (res*j + i)*3; 
            if (noise > 0) {
                ret[c+0] = col_r1;//58;
                // img[ci+0] = col_r1;//58;
                ret[c+1] = col_g1;//50;
                // img[ci+1] = col_g1;//50;
                ret[c+2] = col_b1;//168;
                // img[ci+2] = col_b1;//168;

            } else {
                ret[c+0] = col_r2;//24;
                // img[ci+0] = col_r2;//24;
                ret[c+1] = col_g2;//117;
                // img[ci+1] = col_g2;//117;
                ret[c+2] = col_b2;//22;
                // img[ci+2] = col_b2;//22;
            }

            // double ll = ((noise/2.0f)+0.5f)*256.0;
            // int l = ((noise/2.0f)+0.5f)*255.0;
            // ret[c+0] = l;//randint(10, 240);
            // img[ci+0] = l;//randint(10, 240);
            // ret[c+1] = l;//randint(10, 240);
            // img[ci+1] = l;//randint(100, 240);
            // ret[c+2] = l;//randint(10, 240);
            // img[ci+2] = l;//randint(10, 240);

        }
    }


    return ret;
}





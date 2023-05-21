int pot[] = { A0, A1, A2, A3, A4 };  /////// declarar los potenciometros
int ledsClases[] = { 3, 4, 5, 6 };   //posicion de led en el arreglo ledsClases: agua, planta, fuego, roca
int ledsOutliers[] = { 10, 11 };
int i;
void setup() {
  Serial.begin(9600);
  for (i = 0; i < 5; i++) {
    pinMode(pot[i], INPUT);
    if (i < 4) {
      pinMode(ledsClases[i], OUTPUT);
    }
    if (i < 2) {
      pinMode(ledsClases[i], OUTPUT);
    }
  }
}
String cadenaLeida, vProblema = "";
//String vProblema;
//String cadenaLeida = "p+005+100+f", vProblema; //p+001+001+f
//String cadenaLeida = "p+005+010+f", vProblema; //p+001+001+f
//String cadenaLeida = "p+000+fueg+f"; //cuando no es outlier
//String cadenaLeida = "p+000+plan+f"; //cuando no es outlier
//String cadenaLeida = "p+000+agua+f"; //cuando no es outlier
//String cadenaLeida = "p+000+roca+f"; //cuando no es outlier
//String cadenaLeida = "p+001+f"; //cuando es outlier en iqr leve o punto z
//String cadenaLeida = "p+002+f"; //cuando es outlier en iqr extremo

void loop() {

  if (Serial.available() > 0) {
    cadenaLeida = Serial.readString();
    vProblema="";
    if (cadenaLeida.length() == 11) {
      vProblema = "";
      if (cadenaLeida.substring(0, 1) == "p" && cadenaLeida.substring(10) == "f") {
        int caso = 0, tam = 0;
        caso = cadenaLeida.substring(2, 5).toInt();
        tam = cadenaLeida.substring(6, 9).toInt();

        if (tam > 1) {  /////////////////////////////////////////////////////////si es mas de 1 dato para preprocesar
          switch (caso) {
            case 1:  ////////////////////////////////////////////////////////////promedio
              vProblema = promedio(tam);
              break;
            case 2:  /////////////////////////////////////////////////////////////////mediana
              vProblema = mediana(tam);
              break;
            case 3:  /////////////////////////////////////////////////////7////////////valMax
              vProblema = valMax(tam);
              break;
            case 4:  /////////////////////////////////////////////////////////////////////valMin
              vProblema = valMin(tam);
              break;
            case 5:  ///////////////////////////////////////////////////////////////////////moda
              vProblema = moda(tam);
              break;
          }
        } else {  /////////////////////////////////////////////////////////cuando es solo un dato
          vProblema = muestraUnica(tam);
        }
      }
      vProblema = "r" + vProblema + ",f";
      Serial.println(vProblema);
      delay(10);
    } else if (cadenaLeida.length() == 7) {
      if (cadenaLeida.substring(0, 1) == "p" && cadenaLeida.substring(6) == "f") {
        int led = cadenaLeida.substring(2, 5).toInt();
        for (i = 0; i < led; i++) {
          digitalWrite(ledsOutliers[i], 1);
        }
      }
    } else if (cadenaLeida.length() == 12) {
      Serial.println("entro");
      String clase;
      if (cadenaLeida.substring(0, 1) == "p" && cadenaLeida.substring(10) == "f")
        //agua, fueg, tier, aire
        //tomar el string de la posicion 6 a la 10
        //encender el led de acuerdo
        Serial.println("entro");

      clase = cadenaLeida.substring(6, 10);
      for (i = 0; i < 10; i++) {
        if (clase == "Agua") {
          digitalWrite(ledsClases[0], 1);
        } else if (clase == "Plan") {
          digitalWrite(ledsClases[1], 1);
        } else if (clase == "Fueg") {
          digitalWrite(ledsClases[2], 1);
        } else if (clase == "Roca") {
          digitalWrite(ledsClases[3], 1);
        }
        delay(500);
      }
    }
  }


  for (i = 0; i < 4; i++) {
    digitalWrite(ledsClases[i], 0);
    if (i < 2) {
      digitalWrite(ledsOutliers[i], 0);
    }
  }
  delay(500);
}

///////////////////////////funciones de preprocesamiento///////////////////////////////////////

String promedio(int t) {  ////////////////////////////////////Promedio
  int i, j;
  int valor = 0;
  String v = "";
  for (i = 0; i < 5; i++) {
    for (j = 0; j < t; j++) {
      valor += map(analogRead(pot[i]), 0, 1024, 0, 100);
      //valor += random(1, 100);
    }
    valor /= t;
    v = v + "," + valor;
  }
  return v;
}

String mediana(int t) {
  int i, j, k;
  int mediana;
  String v = "";
  for (k = 0; k < 5; k++) {
    int datos[t];
    mediana = 0.0;
    for (i = 0; i < t; i++) {
      datos[i] = map(analogRead(pot[k]), 0, 1024, 0, 100);
      //datos[i] = random(1, 100);
    }
    for (i = 0; i < t - 1; i++) {  //acomodar muestra
      for (j = 0; j < (t - 1); j++) {
        if (datos[j] > datos[j + 1]) {
          int aux = datos[j];
          datos[j] = datos[j + 1];
          datos[j + 1] = aux;
        }
      }
    }

    int m = int(t / 2);

    if (t % 2 == 0) {
      mediana = (datos[m - 1] + datos[m]) / 2;
    } else {
      mediana = datos[m];
    }
    v = v + "," + mediana;
  }
  return v;
}
//cristian
String valMax(int t) {  ////////////////////////////valor maximo
  int valor = 0;
  int valMax, i, j;
  String v = "";
  for (i = 0; i < 5; i++) {
    valMax = -1;
    for (j = 0; j < t; j++) {
      valor = map(analogRead(pot[i]), 0, 1024, 0, 100);
      //valor = random(1, 100);
      if (valor > valMax) {
        valMax = valor;
      }
    }
    v = v + "," + valMax;
  }
  return v;
}

String valMin(int t) {  /////////////////////////////////valor minimo
  int valor = 0;
  int i, j, valMin;
  String v = "";

  for (i = 0; i < 5; i++) {
    valMin = 9999;
    for (j = 0; j < t; j++) {
      valor = map(analogRead(pot[i]), 0, 1024, 0, 100);
      //valor = random(1, 100);
      if (valor < valMin) {
        valMin = valor;
      }
    }
    v = v + "," + valMin;
  }
  return v;
}

String moda(int t) {  //////////////////////////////////////////moda
  int valor = 0, vecesNuev, vecesAnt, vecesMax, i, j, k;
  String moda, v = "";
  for (k = 0; k < 5; k++) {
    moda = "";
    int datos[t];
    for (i = 0; i < t; i++) {
      datos[i] = map(analogRead(pot[k]),0,1024,0,100);
      //datos[i] = random(1, 100);
    }
    for (i = 0; i < t - 1; i++) {
      for (j = 0; j < (t - 1); j++) {
        if (datos[j] > datos[j + 1]) {
          int aux = datos[j];
          datos[j] = datos[j + 1];
          datos[j + 1] = aux;
        }
      }
    }

    valor = datos[0];
    vecesNuev = 1;
    vecesAnt = 0;
    for (i = 1; i < t; i++) {
      if (valor == datos[i]) {
        vecesNuev++;
      } else {
        if (vecesNuev > vecesAnt) {
          vecesAnt = vecesNuev;
        }
        valor = datos[i];
        vecesNuev = 1;
      }
    }

    if (vecesNuev > vecesAnt) {
      vecesMax = vecesNuev;
    } else {
      vecesMax = vecesAnt;
    }
    valor = datos[0];
    vecesNuev = 1;
    moda = "";
    if (vecesMax == 1) {
      int r = random(1, t);
      moda = datos[r];
    }
    for (i = 1; i < t; i++) {
      if (valor == datos[i]) {
        vecesNuev++;
        if (vecesNuev == vecesMax) {
          moda = valor;
        }
      } else {
        valor = datos[i];
        vecesNuev = 1;
      }
    }
    v = v + "," + moda;
  }
  return v;
}

String muestraUnica(int t) {  ////////////////////////////muestra unica
  int i;
  String v = "";
  for (i = 0; i < 5; i++) {
    v = v + "," + map(analogRead(pot[i]), 0, 1024, 0, 100);
    //v = v + "," + String(random(1, 100));
  }
  return v;
}

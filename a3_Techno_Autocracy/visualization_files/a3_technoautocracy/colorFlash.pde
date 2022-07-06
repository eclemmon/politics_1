import java.util.ArrayList;

public void flash(ColorScheme color_scheme) {
  Color clr;
  for(int x = 0; x < 8; x++) {
    for (int y = 0; y<4; y++) {
      clr = color_scheme.choose();
      clr.fill_color();
      rect(240*x,240*y, 240, 240);
    };

  };

};

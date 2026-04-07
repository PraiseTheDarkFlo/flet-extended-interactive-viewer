import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'flet_extended_interactive_viewer.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "FletExtendedInteractiveViewer":
        return FletExtendedInteractiveViewerControl(
            control: control);
      default:
        return null;
    }
  }
}

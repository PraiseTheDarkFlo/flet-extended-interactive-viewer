import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'dart:convert';

//main class
class FletExtendedInteractiveViewerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const FletExtendedInteractiveViewerControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.backend,
  });

  @override
  State<FletExtendedInteractiveViewerControl> createState() =>
      _FletExtendedInteractiveViewerControlState();
}

//State control with state attributes
class _FletExtendedInteractiveViewerControlState extends State<FletExtendedInteractiveViewerControl> with SingleTickerProviderStateMixin{

  final TransformationController _transformationController = TransformationController();
  late AnimationController _animationController;
  Animation<Matrix4>? _animation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(vsync: this, duration: Duration.zero);
    widget.backend.subscribeMethods(widget.control.id, _onMethodCall);
  }

  //Catches method call which comes from the python file
   Future<String?> _onMethodCall(String method_name, Map<String, String> args) async {
    switch (method_name) {
      case "zoom":
        var factor = parseDouble(args["factor"]);
        if (factor != null) {
          _transformationController.value =
              _transformationController.value.scaled(factor, factor);
        }
        return null;
      case "reset":
        var animationDuration = Duration(milliseconds: int.tryParse(args["animation_duration"] ?? "0") ?? 0);
        if (animationDuration == 0) {
          _transformationController.value = Matrix4.identity();
        } else {
          _animationController.duration = animationDuration;
          _animation = Matrix4Tween(
            begin: _transformationController.value,
            end: Matrix4.identity(),
          ).animate(_animationController)
            ..addListener(() {
              _transformationController.value = _animation!.value;
            });
          _animationController.forward(from: 0);
        }
        return null;
      default:
        throw Exception("Unknown ExtendedInteractiveViewer method: $method_name");
    }
  }

  //clean up method
  @override
  void dispose() {
    _transformationController.dispose();
    _animationController.dispose();
    //unsubscribe so no longer methode call gets forwarded
    widget.backend.unsubscribeMethods(widget.control.id);
    super.dispose();
  }

  //build content methode
  @override
  Widget build(BuildContext context) {
    final contentCtrls = widget.children
    .where((c) => c.name == "content" && c.isVisible)
    .toList();

    final disabled = widget.control.isDisabled || widget.parentDisabled;

    Widget? content_widget;
    if (contentCtrls.isNotEmpty) {
      content_widget = createControl(widget.control,contentCtrls.first.id, disabled);
    }

    Widget interactive_viewer = InteractiveViewer(
        transformationController: _transformationController,
        boundaryMargin: EdgeInsets.zero,
        minScale: widget.control.attrDouble("max_scale",2.5)!,
        maxScale: widget.control.attrDouble("min_scale",0.8)!,
        scaleEnabled: widget.control.attrBool("scale_enabled", true)!,
        scaleFactor: widget.control.attrDouble("scale_factor", 200)!,
        constrained: widget.control.attrBool("constrained", true)!,
        onInteractionUpdate: !widget.control.isDisabled
          ? (ScaleUpdateDetails details) {
              final translation = _transformationController.value.getTranslation();
              double offset_x = translation.x;
              double offset_y = translation.y;
              double scale = _transformationController.value.getMaxScaleOnAxis();
              final eventData = {
                "offset_x": offset_x,
                "offset_y": offset_y,
                "scale": scale,
              };
              widget.backend.triggerControlEvent(widget.control.id,"interaction_update", json.encode(eventData));
            }
          : null,
        child: content_widget ?? const ErrorControl(
              "InteractiveViewer.content must be provided and visible"),
    );

    return constrainedControl(context,interactive_viewer,widget.parent,widget.control);
  }
}

import 'dart:math' as math;

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'dart:convert';

class _ChildSize extends StatefulWidget {
  final Widget child;
  final Function(Size) onSizeChanged;

  const _ChildSize({
    required this.child,
    required this.onSizeChanged,
  });

  @override
  State<_ChildSize> createState() => _ChildSizeState();
}

class _ChildSizeState extends State<_ChildSize> {
  Size? _lastSize;

  @override
  Widget build(BuildContext context) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final currentSize = context.size;
      if (currentSize != null && _lastSize != currentSize) {
        _lastSize = currentSize;
        widget.onSizeChanged(currentSize);
      }
    });
    return widget.child;
  }
}

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
  bool _ignoreTransformationChange = false;
  bool _ignorScroll = false;
  final ScrollController _horizontalScrollController = ScrollController();
  final ScrollController _verticalScrollController = ScrollController();
  Size? _childSize;
  Size? _viewportSize;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(vsync: this, duration: Duration.zero);
    widget.backend.subscribeMethods(widget.control.id, _onMethodCall);
    _transformationController.addListener(_onTransformationChanged);
    _horizontalScrollController.addListener(_onScroll);
    _verticalScrollController.addListener(_onScroll);
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
      case "get_transformation_data":
        final translation = _transformationController.value.getTranslation();
        double offset_x = translation.x;
        double offset_y = translation.y;
        double scale = _transformationController.value.getMaxScaleOnAxis();
        final eventData = {
          "offset_x": offset_x,
          "offset_y": offset_y,
          "scale": scale,
        };
        return  json.encode(eventData);
      case "set_transformation_data":
        var off_set_x = parseDouble(args["offSetX"],0)!;
        var off_set_y = parseDouble(args["offSetY"],0)!;
        var scale = parseDouble(args["scale"],1)!;

        double contentWidth = _childSize!.width * scale;
        double contentHeight = _childSize!.height * scale;

        double maxScrollX = math.max(0, contentWidth - _viewportSize!.width);
        double maxScrollY = math.max(0, contentHeight - _viewportSize!.height);

        double scrollX = (-off_set_x).clamp(0.0, maxScrollX);
        double scrollY = (-off_set_y).clamp(0.0, maxScrollY);
        Matrix4 newMatrix = Matrix4.identity()
        ..scale(scale, scale)
        ..translate(-scrollX / scale, -scrollY / scale);
        _transformationController.value = newMatrix;
        return null;
      case "reset":
        var animationDuration = Duration(milliseconds: int.tryParse(args["duration"] ?? "0") ?? 0);
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

  void _onTransformationChanged() {
    if (_ignoreTransformationChange) return;
    if (_viewportSize == null || _childSize == null) return;

    final translation = _transformationController.value.getTranslation();
    double scale = _transformationController.value.getMaxScaleOnAxis();

    double contentWidth = _childSize!.width * scale;
    double contentHeight = _childSize!.height * scale;

    double maxScrollX = math.max(0, contentWidth - _viewportSize!.width);
    double maxScrollY = math.max(0, contentHeight - _viewportSize!.height);

    double scrollX = (-translation.x).clamp(0.0, maxScrollX);
    double scrollY = (-translation.y).clamp(0.0, maxScrollY);

    _ignorScroll = true;
    _horizontalScrollController.jumpTo(scrollX);
    _verticalScrollController.jumpTo(scrollY);
    _ignorScroll = false;
  }

  void _onScroll() {
    if (_ignorScroll) return;
    if (_viewportSize == null || _childSize == null) return;
    double scrollX = 0;
    double scrollY = 0;
    if (_horizontalScrollController.hasClients) {
      scrollX = _horizontalScrollController.position.pixels;
    }
    if (_verticalScrollController.hasClients) {
      scrollY = _verticalScrollController.position.pixels;
    }
    double scale = _transformationController.value.getMaxScaleOnAxis();

    _ignoreTransformationChange = true;
    Matrix4 newMatrix = Matrix4.identity()
    ..scale(scale, scale)
    ..translate(-scrollX / scale, -scrollY / scale);
    _transformationController.value = newMatrix;
    _ignoreTransformationChange = false;
  }

  void _onChildSizeChanged(Size size) {
    if (size != _childSize) {
      setState(() {
        _childSize = size;
      });
      _onTransformationChanged();
    }
  }

  //clean up method
  @override
  void dispose() {
    _transformationController.removeListener(_onTransformationChanged);
    _transformationController.dispose();
    _animationController.dispose();
    _verticalScrollController.removeListener(_onScroll);
    _verticalScrollController.dispose();
    _horizontalScrollController.removeListener(_onScroll);
    _horizontalScrollController.dispose();

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

    Widget interactive_viewer = LayoutBuilder(
      builder: (context, constraints) {
        _viewportSize = Size(constraints.maxWidth, constraints.maxHeight);
        WidgetsBinding.instance.addPostFrameCallback((_) {
          if (mounted) {
            _onTransformationChanged();
          }
        });

        return InteractiveViewer(
          transformationController: _transformationController,
          boundaryMargin: EdgeInsets.zero,
          minScale: widget.control.attrDouble("maxScale", 2.5)!,
          maxScale: widget.control.attrDouble("minScale", 0.8)!,
          panEnabled: widget.control.attrBool("panEnabled", true)!,
          scaleEnabled: widget.control.attrBool("scaleEnabled", true)!,
          scaleFactor: widget.control.attrDouble("scaleFactor", 200)!,
          constrained: widget.control.attrBool("constrained", true)!,
          onInteractionUpdate: !widget.control.isDisabled
              ? (ScaleUpdateDetails details) {
            final translation = _transformationController.value
                .getTranslation();
            double offset_x = translation.x;
            double offset_y = translation.y;
            double scale = _transformationController.value.getMaxScaleOnAxis();
            final eventData = {
              "offset_x": offset_x,
              "offset_y": offset_y,
              "scale": scale,
            };
            widget.backend.triggerControlEvent(
                widget.control.id, "interaction_update",
                json.encode(eventData));
          }
              : null,
          child: _ChildSize(
            onSizeChanged: _onChildSizeChanged,
            child: content_widget ??
                const ErrorControl(
                    "InteractiveViewer.content must be provided and visible"),
          ),
        );
      },
    );
    double scale = _transformationController.value.getMaxScaleOnAxis();
    double contentWidth = _childSize != null ? _childSize!.width * scale : 0;
    double contentHeight = _childSize != null ? _childSize!.height * scale : 0;

    double maxScrollX = math.max(0, contentWidth - (_viewportSize?.width ?? 0));
    double maxScrollY = math.max(0, contentHeight - (_viewportSize?.height ?? 0));

    bool check_spawn_x = (maxScrollX > 0 && widget.control.attrBool("xScrollEnabled",true)!);
    bool check_spawn_y = (maxScrollY > 0 &&  widget.control.attrBool("yScrollEnabled",true)!);

     Widget scrollableContent = Stack(
      children: [
        Positioned.fill(child: interactive_viewer),

        if (check_spawn_x)
          Positioned(
            left: 0,
            right: check_spawn_y ? 12 : 0,
            bottom: 0,
            child: SizedBox(
              height: 12,
              child: Scrollbar(
                controller: _horizontalScrollController,
                thumbVisibility: true,
                child: SingleChildScrollView(
                  controller: _horizontalScrollController,
                  scrollDirection: Axis.horizontal,
                  physics: widget.control.attrBool("interactiveScrollEnabled", true)!
                  ? const AlwaysScrollableScrollPhysics()
                  : const NeverScrollableScrollPhysics(),
                  child: SizedBox(
                    width: check_spawn_y? contentWidth-12:contentWidth,
                    height: 1,
                  ),
                ),
              ),
            ),
          ),

        if (check_spawn_y)
          Positioned(
            top: 0,
            right: 0,
            bottom: check_spawn_x ? 12 : 0,
            child: SizedBox(
              width: 12,
              child: Scrollbar(
                controller: _verticalScrollController,
                thumbVisibility: true,
                child: SingleChildScrollView(
                  controller: _verticalScrollController,
                  scrollDirection: Axis.vertical,
                  physics: widget.control.attrBool("interactiveScrollEnabled", true)!
                  ? const AlwaysScrollableScrollPhysics()
                  : const NeverScrollableScrollPhysics(),
                  child: SizedBox(
                    width: 1,
                    height: check_spawn_x? contentHeight-12:contentHeight,
                  ),
                ),
              ),
            ),
          ),
      ],
    );

    return constrainedControl(context,scrollableContent,widget.parent,widget.control);
  }
}

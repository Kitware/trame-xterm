import "xterm/css/xterm.css";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";

const EVENT_TO_METHOD = {
  bell: "onBell",
  binary: "onBinary",
  cursorMove: "onCursorMove",
  input: "onData",
  key: "onKey",
  lineFeed: "onLineFeed",
  render: "onRender",
  writeParsed: "onWriteParsed",
  resize: "onResize",
  scroll: "onScroll",
  selectionChange: "onSelectionChange",
  titleChange: "onTitleChange",
};

export default {
  props: {
    options: {
      type: Object,
    },
    listen: {
      type: Array,
      default: () => ["input"],
    },
  },
  emits: [
    // lifecycle
    "opened",
    "disposed",
    // xterm.js
    "bell",
    "binary",
    "cursorMove",
    "input",
    "key",
    "lineFeed",
    "render",
    "writeParsed",
    "resize",
    "scroll",
    "selectionChange",
    "titleChange",
  ],
  setup(props, { emit, expose }) {
    const elem = ref(null);
    const term = new Terminal(props.options);
    const fitAddon = new FitAddon();

    function fit() {
      fitAddon.fit();
    }

    const sizeObserver = new ResizeObserver(fit);
    term.loadAddon(fitAddon);

    // Events
    for (let i = 0; i < props.listen.length; i++) {
      const eventName = props.listen[i];
      const methodName = EVENT_TO_METHOD[eventName];
      if (eventName === "selectionChange") {
        term[methodName](() =>
          emit(eventName, {
            hasSelection: term.hasSelection() ? 1 : 0,
            selection: term.getSelection(),
            position: term.getSelectionPosition(),
          })
        );
      } else if (methodName) {
        term[methodName]((e) => emit(eventName, e));
      }
    }

    // Methods
    const methods = {
      fit,
      // Skipped: open, dispose, loadAddon, +Experimental
      blur() {
        return term.blur();
      },
      focus() {
        return term.focus();
      },
      resize(columns, rows) {
        return term.resize(columns, rows);
      },
      attachCustomKeyEventHandler(handler) {
        return term.attachCustomKeyEventHandler(handler);
      },
      registerLinkProvider(linkProvider) {
        return term.registerLinkProvider(linkProvider);
      },
      registerMarker(cursorYOffset) {
        return term.registerMarker(cursorYOffset);
      },
      registerDecoration(decorationOptions) {
        return term.registerDecoration(decorationOptions);
      },
      hasSelection() {
        return term.hasSelection();
      },
      getSelection() {
        return term.getSelection();
      },
      getSelectionPosition() {
        return term.getSelectionPosition();
      },
      clearSelection() {
        return term.clearSelection();
      },
      select(column, row, length) {
        return term.select(column, row, length);
      },
      selectAll() {
        return term.selectAll();
      },
      selectLines(start, end) {
        return term.selectLines(start, end);
      },
      scrollLines(amount) {
        return term.scrollLines(amount);
      },
      scrollPages(pageCount) {
        return term.scrollPages(pageCount);
      },
      scrollToTop() {
        return term.scrollToTop();
      },
      scrollToBottom() {
        return term.scrollToBottom();
      },
      scrollToLine(line) {
        return term.scrollToLine(line);
      },
      clear() {
        return term.clear();
      },
      write(data, callback) {
        return term.write(data, callback);
      },
      writeln(data, callback) {
        return term.writeln(data, callback);
      },
      paste(data) {
        return term.paste(data);
      },
      refresh(start, end) {
        return term.refresh(start, end);
      },
      clearTextureAtlas() {
        return term.clearTextureAtlas();
      },
      reset() {
        return term.reset();
      },
    };

    onMounted(() => {
      term.open(elem.value);
      sizeObserver.observe(elem.value);
      emit("opened");
    });

    onBeforeUnmount(() => {
      sizeObserver.unobserve(elem.value);
      term.dispose();
      emit("disposed");
    });

    expose(methods);
    return { ...methods, elem };
  },
  template: `<div style="position: relative; width: 100%; height: 100%;" v-bind="$attrs">
      <div ref="elem" style="position: absolute; width: 100%; height: 100%;"></div>
    </div>
    `,
};

import { s as styleTags, t as tags, f as foldNodeProp, c as foldInside, p as parseMixed, S as StreamLanguage } from './Index19-A6-Y_zIL.js';
import { yaml } from './yaml-BZBlrf2X.js';
import './ssr-Cz1f32Mr.js';
import './2-BZ3PdVP1.js';
import './index4-D_FyJKAV.js';
import './Download-BYY54H3I.js';
import './DownloadLink-Crj4dtQe.js';
import './file-url-D-K40zdU.js';
import './IconButtonWrapper-A6xfjAju.js';
import './Code-CNhFvcVb.js';
import './BlockLabel-u4I5nFh_.js';
import './Empty-B3TFLl4E.js';
import './Example10-DNx5uJIG.js';

const frontMatterFence = /^---\s*$/m;
const frontmatter = {
  defineNodes: [{ name: "Frontmatter", block: true }, "FrontmatterMark"],
  props: [
    styleTags({
      Frontmatter: [tags.documentMeta, tags.monospace],
      FrontmatterMark: tags.processingInstruction
    }),
    foldNodeProp.add({
      Frontmatter: foldInside,
      FrontmatterMark: () => null
    })
  ],
  wrap: parseMixed((node) => {
    const { parser } = StreamLanguage.define(yaml);
    if (node.type.name === "Frontmatter") {
      return {
        parser,
        overlay: [{ from: node.from + 4, to: node.to - 4 }]
      };
    }
    return null;
  }),
  parseBlock: [
    {
      name: "Frontmatter",
      before: "HorizontalRule",
      parse: (cx, line) => {
        let end = void 0;
        const children = new Array();
        if (cx.lineStart === 0 && frontMatterFence.test(line.text)) {
          children.push(cx.elt("FrontmatterMark", 0, 4));
          while (cx.nextLine()) {
            if (frontMatterFence.test(line.text)) {
              end = cx.lineStart + 4;
              break;
            }
          }
          if (end !== void 0) {
            children.push(cx.elt("FrontmatterMark", end - 4, end));
            cx.addElement(cx.elt("Frontmatter", 0, end, children));
          }
          return true;
        }
        return false;
      }
    }
  ]
};

export { frontmatter };
//# sourceMappingURL=frontmatter-RLhTWdV2.js.map

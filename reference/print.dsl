<!DOCTYPE style-sheet PUBLIC "-//James Clark//DTD DSSSL Style Sheet//EN" [
<!ENTITY docbook PUBLIC "-//Norman Walsh//DOCUMENT DocBook Print Stylesheet//EN" CDATA DSSSL>
<!ENTITY citation SYSTEM "citation.dsl" CDATA DSSSL>
]>
<style-sheet>
<style-specification id="print" use="citation docbook">
<style-specification-body>

(define %section-autolabel% #t)
(define %default-quadding% 'justify)
(define %mono-font-family% "Courier")
(define %callout-fancy-bug% #t)

(element subscript (process-children))
(element superscript (process-children))

(element application 
  ($mono-seq$))

(element phrase 
  (if (and (attribute-string (normalize "role"))
	   (or (equal? (attribute-string (normalize "role")) "strong")
	       (equal? (attribute-string (normalize "role")) "bold")))
      ($bold-mono-seq$)
      (process-children)))

</style-specification-body>
</style-specification>
<external-specification id="docbook" document="docbook">
<external-specification id="citation" document="citation">
</style-sheet>

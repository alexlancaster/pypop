<!DOCTYPE style-sheet PUBLIC "-//James Clark//DTD DSSSL Style Sheet//EN"[
<!ENTITY docbook PUBLIC "-//Norman Walsh//DOCUMENT DocBook Print Stylesheet//EN" CDATA DSSSL>
]>
<style-sheet>
<style-specification id="print" use="docbook">
<style-specification-body>

(element citation 
  (if biblio-citation-check
      (let* ((bgraphies (select-elements (descendants (sgml-root-element))
					 (normalize "bibliography")))
	     (bchildren1 (expand-children bgraphies
					  (list (normalize "bibliography"))))
	     (bchildren2 (expand-children bchildren1
					  (list (normalize "bibliodiv"))))
	     (type (attribute-string (normalize "role")))
	     (bibentries (node-list-filter-by-gi 
			  bchildren2
			  (list (normalize "biblioentry")
				(normalize "bibliomixed")))))

	(let loop ((bibs bibentries))

	  (if (node-list-empty? bibs)
	      (make sequence
		(error (string-append "Cannot find citation: " 
					   (data (current-node))))
		(literal "(") 
		($charseq$) 
		(literal ")")
		)
	      (if (citation-matches-target? (current-node) 
					    (node-list-first bibs))
		  (make link 
		    destination: (node-list-address (node-list-first bibs))
		    ;;(error (string-append "role: " type))
		    ($charseq$
		     (sosofo-append
		      (let* ((elem (children (node-list-first bibs)))
			     (year (select-elements elem (normalize "pubdate")))
			     (citetokens (reverse 
					  (split (data (current-node)))))
			     (yearstring (data year))
			     (authorstring ""))
			
			(cond
			 ((equal? type (normalize "citet"))
			  (make sequence
			    (literal authorstring)
			    (literal " (") 
			    (literal yearstring)
			    (literal ")")
			    ))
			 ((equal? type (normalize "citeyear"))
			  (make sequence
			    (literal yearstring)
			    ))
			 ((equal? type (normalize "citeyearpar"))
			  (make sequence
			    (literal "(")
			    (literal yearstring)
			    (literal ")")
			    ))
			 ((equal? type (normalize "citealt"))
			  (make sequence 
			    (process-children)
			    ))
			 (else
			  (make sequence
			    (literal "(")
			    (process-children)
			    (literal ")")))))))
		    )
		  (loop (node-list-rest bibs))))))
      (make sequence 
	(literal "(") ($charseq$) (literal ")"))))


(define (en-author-string #!optional (author (current-node)))
  ;; Return a formatted string representation of the contents of:
  ;; AUTHOR:
  ;;   Handles Honorific, FirstName, SurName, and Lineage.
  ;;     If %author-othername-in-middle% is #t, also OtherName
  ;;   Handles *only* the first of each.
  ;;   Format is "Honorific. FirstName [OtherName] SurName, Lineage"
  ;; CORPAUTHOR:
  ;;   returns (data corpauthor)
  (let* ((h_nl (select-elements (descendants author) (normalize "honorific")))
	 (f_nl (select-elements (descendants author) (normalize "firstname")))
	 (o_nl (select-elements (descendants author) (normalize "othername")))
	 (s_nl (select-elements (descendants author) (normalize "surname")))
	 (l_nl (select-elements (descendants author) (normalize "lineage")))
	 (has_h (not (node-list-empty? h_nl)))
	 (has_f (not (node-list-empty? f_nl)))
	 (has_o (and %author-othername-in-middle%
		     (not (node-list-empty? o_nl))))
	 (has_s (not (node-list-empty? s_nl)))
	 (has_l (not (node-list-empty? l_nl))))
    (if (or (equal? (gi author) (normalize "author"))
	    (equal? (gi author) (normalize "editor"))
	    (equal? (gi author) (normalize "othercredit")))
	(string-append
	 (if has_h (string-append (data-of (node-list-first h_nl)) 
				  %honorific-punctuation%) "")
	 ;; put surname first
	 (if has_s (string-append 
		    (if (or has_h has_f has_o) " " "")
		    (data-of (node-list-first s_nl))) "")
	 ;; only get first character of firstname
	 (if has_f (string-append 
		    (if (or has_h has_s) " " "") 
		    (substring (data-of (node-list-first f_nl)) 0 1)) "")
	 (if has_o (string-append
		    (if (or has_h has_f) "" "")
		    (data-of (node-list-first o_nl))) "")
	 (if has_l (string-append ", " (data-of (node-list-first l_nl))) ""))
	(data-of author))))

; (element biblioentry
;   (let* ((expanded-children   (expand-children 
; 			       (children (current-node))
; 			       (biblioentry-flatten-elements)))
; 	 (all-inline-children (if %biblioentry-in-entry-order%
; 				  (titlepage-gi-list-by-nodelist
; 				   (biblioentry-inline-elements)
; 				   expanded-children)
; 				  (titlepage-gi-list-by-elements
; 				   (biblioentry-inline-elements)
; 				   expanded-children)))
; 	 (block-children      (if %biblioentry-in-entry-order%
; 				  (titlepage-gi-list-by-nodelist
; 				   (biblioentry-block-elements)
; 				   expanded-children)
; 				  (titlepage-gi-list-by-elements
; 				   (biblioentry-block-elements)
; 				   expanded-children)))
; 	 (leading-abbrev      (if (equal? (normalize "abbrev")
; 					  (gi (node-list-first 
; 					       all-inline-children)))
; 				  (node-list-first all-inline-children)
; 				  (empty-node-list)))
; 	 (inline-children     (if (node-list-empty? leading-abbrev)
; 				  all-inline-children
; 				  (node-list-rest all-inline-children)))
; 	 (has-leading-abbrev? (not (node-list-empty? leading-abbrev)))
; 	 (xreflabel           (if (or has-leading-abbrev? biblio-number)
; 				  #f
; 				  (attribute-string (normalize "xreflabel")))))
;     (make display-group
;       (make paragraph
; 	space-before: %para-sep%
; 	space-after: %para-sep%
; 	start-indent: (+ (inherited-start-indent) 2pi)
; 	first-line-start-indent: -2pi

; ;;	(if (or biblio-number xreflabel has-leading-abbrev?)
; ;;	    (make sequence
; ;;	      (literal "[")
; ;;
; ;;	      (if biblio-number 
; ;;		  (literal (number->string (bibentry-number (current-node))))
; ;;		  (empty-sosofo))
; ;;	
; ;;	      (if xreflabel
; ;;		  (literal xreflabel)
; ;;		  (empty-sosofo))
; ;;	
; ;;	      (if has-leading-abbrev?
; ;;		  (with-mode biblioentry-inline-mode 
; ;;		    (process-node-list leading-abbrev))
; ;;		  (empty-sosofo))
; ;;
; ;;	      (literal "]\no-break-space;"))
; ;;	    (empty-sosofo))

; 	(let loop ((nl inline-children))
; 	  (if (node-list-empty? nl)
; 	      (empty-sosofo)
; 	      (make sequence
; 		(with-mode biblioentry-inline-mode
; 		  (process-node-list (node-list-first nl)))
; 		(if (node-list-empty? (node-list-rest nl))
; 		    (biblioentry-inline-end block-children)
; 		    (biblioentry-inline-sep (node-list-first nl)
; 					  (node-list-rest nl)))
; 		(loop (node-list-rest nl))))))

;       (make display-group
; 	start-indent: (+ (inherited-start-indent) 2pi)
; 	(let loop ((nl block-children))
; 	  (if (node-list-empty? nl)
; 	      (empty-sosofo)
; 	      (make sequence
; 		(with-mode biblioentry-block-mode
; 		  (process-node-list (node-list-first nl)))
; 		(if (node-list-empty? (node-list-rest nl))
; 		    (biblioentry-block-end)
; 		    (biblioentry-block-sep (node-list-first nl)
; 					   (node-list-rest nl)))
; 		(loop (node-list-rest nl)))))))))


(mode biblioentry-inline-mode
  (element volumenum ($bold-seq$))
)

(element citetitle
  (let ((work (attribute-string (normalize "pubwork"))))
    (cond 
     ((or (equal? work (normalize "article"))
	  (equal? work (normalize "chapter")))
      (make sequence
        (literal (gentext-start-quote))
        (process-children-trim)
          (literal (gentext-end-quote))))
     (else ($italic-seq$)))))

(mode biblioentry-inline-mode
  (element editor
    (make sequence
      (if (first-sibling?) 
	  (make sequence
	    (literal (gentext-edited-by))
	    (literal " "))
	  (empty-sosofo))
      (literal (author-list-string))))
  (element issuenum
    (make sequence
      (literal "(")
      (process-children)
      (literal ")"))))

(define (biblioentry-inline-sep node rest)
  ;; Output the character that should separate inline node from rest
  (cond 
   ((and (equal? (gi node) (normalize "volumenum"))
	 (equal? (gi (node-list-first rest)) (normalize "pagenums")))
      (literal ": "))
   (else
    (literal %biblsep%))))


</style-specification-body>
</style-specification>
<external-specification id="docbook" document="docbook">
</style-sheet>

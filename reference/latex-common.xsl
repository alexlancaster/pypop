<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version='1.0'>

 <xsl:import href="http://db2latex.sourceforge.net/docbook.xsl"/>

 <xsl:output method="text" encoding="ISO-8859-1" indent="yes"/>

 <!-- set default language to English (en) -->
 <xsl:param name="l10n.gentext.language" select="'en'"/>

 <xsl:template match="ackno">
  <xsl:call-template name="map.begin"/>
  <xsl:apply-templates/>
  <xsl:call-template name="map.end"/>
 </xsl:template>

 <!-- a better <ulink>, that doesn't output the link twice if "url" attrib
   and <ulink> contents are identical, doesn't use the \urldef which seems 
   to be broken -->
 <xsl:template match="ulink">
  <xsl:variable name="url">
   <xsl:text>{\tt </xsl:text>   
   <xsl:value-of select="@url"/> 
   <xsl:text>}</xsl:text>
  </xsl:variable>

  <xsl:choose>
   <xsl:when test=".!=@url">
    <xsl:apply-templates mode="slash.hyphen"/>
    <xsl:text> (</xsl:text>
    <xsl:value-of select="$url"/>
    <xsl:text>)</xsl:text>
   </xsl:when>
   <xsl:otherwise>
    <xsl:value-of select="$url"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <xsl:template match="citation">
  <!-- todo: biblio-citation-check -->
  <xsl:text>~\cite{</xsl:text>
  <xsl:apply-templates/>
  <xsl:text>}</xsl:text>
 </xsl:template>

 <!-- more intelligent output template, only generates a tag label
 if requested and handles <citetitle> -->

 <xsl:template name="biblioentry.output">
  
  <xsl:variable name="biblioentry.tag.label">
   <xsl:choose>
   <xsl:when test="$latex.dont.label!=1">
    <xsl:text>[</xsl:text>
    <xsl:choose>
     <xsl:when test="@xreflabel">
      <xsl:value-of select="normalize-space(@xreflabel)"/>
     </xsl:when>
     <xsl:otherwise>
      <xsl:text>UNKNOWN</xsl:text>
     </xsl:otherwise>
    </xsl:choose>
    <xsl:text>]</xsl:text>
   </xsl:when>
    <xsl:otherwise><xsl:text></xsl:text></xsl:otherwise>
   </xsl:choose>
  </xsl:variable>

  <xsl:variable name="biblioentry.tag.id">
   <xsl:text>{</xsl:text>
   <xsl:choose>
    <xsl:when test="abbrev">
     <xsl:apply-templates select="abbrev" mode="bibliography.mode"/>
    </xsl:when>
    <xsl:when test="@id">
     <xsl:value-of select="normalize-space(@id)"/>
    </xsl:when>
    <xsl:otherwise>
     <xsl:text>UNKNOWN</xsl:text>
    </xsl:otherwise>
   </xsl:choose>
   <xsl:text>}</xsl:text>
  </xsl:variable>
  
  <xsl:text>&#10;</xsl:text>
  <xsl:text>% -------------- biblioentry &#10;</xsl:text>
  <xsl:text>\bibitem</xsl:text><xsl:value-of select="$biblioentry.tag.label"/><xsl:value-of select="$biblioentry.tag.id"/>

  <xsl:if test="author|authorgroup">
   <xsl:apply-templates select="author|authorgroup" mode="bibliography.mode"/>
   <xsl:value-of select="$biblioentry.item.separator"/>
  </xsl:if>

  <xsl:apply-templates select="citetitle[@pubwork='refentry']" mode="bibliography.mode"/>  

  <xsl:apply-templates select="citetitle[@pubwork='article']" mode="bibliography.mode"/>
  
  <xsl:apply-templates select="citetitle[@pubwork='journal']" mode="bibliography.mode"/>
  
  <xsl:for-each select="copyright|publisher|isbn">
   <xsl:value-of select="$biblioentry.item.separator"/>
   <xsl:apply-templates select="." mode="bibliography.mode"/> 
  </xsl:for-each>

  <xsl:if test="pubdate">
   <xsl:text> (</xsl:text>
   <xsl:apply-templates select="pubdate" mode="bibliography.mode"/> 
   <xsl:text>)</xsl:text>
  </xsl:if>

  <xsl:text>.</xsl:text>
  
  <xsl:call-template name="label.id"/> 
  <xsl:text>&#10;&#10;</xsl:text>

 </xsl:template>

 <!-- retrieve citation if <citation> tag matches the <biblioentry> "id" -->
 <!-- as well as <abbrev> -->

 <xsl:template match="biblioentry" mode="bibliography.cited">
  <xsl:param name="bibid" select="@id"/>
  <xsl:param name="ab" select="abbrev"/>
  <xsl:variable name="nx" select="//xref[@linkend=$bibid]"/>
  <xsl:variable name="nc" select="//citation[text()=$ab]"/>
  <xsl:variable name="ni" select="//citation[text()=$bibid]"/>
  <xsl:if test="count($nx) &gt; 0 or count($nc) &gt; 0 or count($ni) &gt; 0">
   <xsl:call-template name="biblioentry.output"/>
  </xsl:if>
 </xsl:template>
 
 <xsl:template match="application">
  <xsl:call-template name="map.begin"/>
  <xsl:apply-templates />
  <xsl:call-template name="map.end"/>
 </xsl:template>

 <!-- override these templates, because default ones put extra whitespace
 where we don't want it in the output and where it is significant to LaTeX -->

 <xsl:template name="inline.italicseq">
  <xsl:param name="content"> <xsl:apply-templates/> </xsl:param>
  <xsl:text>{\em </xsl:text>
  <xsl:copy-of select="$content"/> <xsl:text>}</xsl:text>
 </xsl:template>

 <xsl:template name="number.xref">
  <xsl:text> \ref{</xsl:text><xsl:value-of
   select="@id"/><xsl:text>}</xsl:text>
 </xsl:template>

 <xsl:template match="book">
  <xsl:call-template name="generate.latex.book.preamble"/>
  <!-- Output title information -->
  <xsl:text>\title{</xsl:text>
  <xsl:choose>
   <xsl:when test="./title">
    <xsl:value-of select="normalize-space(./title)"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:value-of select="normalize-space(./bookinfo/title)"/>
   </xsl:otherwise>
  </xsl:choose>
  <xsl:text>}&#10;</xsl:text>
  <!-- Output author information -->
  <xsl:text>\author{</xsl:text>
  <xsl:choose>
   <xsl:when test="bookinfo/authorgroup">
    <xsl:apply-templates select="bookinfo/authorgroup"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:apply-templates select="bookinfo/author"/>
   </xsl:otherwise>
  </xsl:choose>
  <xsl:text>}&#10;</xsl:text>

  <xsl:value-of select="$latex.book.afterauthor"/>
  <xsl:text>&#10;\setcounter{tocdepth}{</xsl:text><xsl:value-of select="$toc.section.depth"/><xsl:text>}&#10;</xsl:text>
  <xsl:text>&#10;\setcounter{secnumdepth}{</xsl:text><xsl:value-of select="$section.depth"/><xsl:text>}&#10;</xsl:text>
  <xsl:value-of select="$latex.book.begindocument"/>
  <!-- Include external Cover page if specified -->
  <xsl:text>&#10;\InputIfFileExists{</xsl:text><xsl:value-of select="$latex.titlepage.file"/>
  <xsl:text>}{\typeout{WARNING: Using cover page</xsl:text>
  <xsl:value-of select="$latex.titlepage.file"/>
  <xsl:text>}}</xsl:text>
  <xsl:text>{\maketitle}&#10;</xsl:text>

  <!-- APPLY TEMPLATES -->
  <xsl:apply-templates/>
  <xsl:call-template name="map.end"/>
 </xsl:template>
 
 <!-- fix template: needed space after \hline -->
 <xsl:template match="tgroup">
  <xsl:variable name="align" select="@align"/>
  <xsl:variable name="colspecs" select="./colspec"/>
  <!-- <xsl:text>{\tt </xsl:text> -->
  <xsl:text>\begin{tabular}{</xsl:text>
  <xsl:if test="@frame='' or @frame='all' or @frame='sides'">
   <xsl:text>|</xsl:text>
  </xsl:if>
  <xsl:call-template name="table.format.tabular">
   <xsl:with-param name="cols" select="@cols"/>
  </xsl:call-template>
  <xsl:if test="@frame='' or @frame='all' or @frame='sides'">
   <xsl:text>|</xsl:text>
  </xsl:if>
  <xsl:text>}&#10;</xsl:text>
  <xsl:if test="@frame!='sides' and @frame!='none' and @frame!='bottom'">
   <xsl:text>\hline &#10;</xsl:text>
  </xsl:if>
  <!-- APPLY TEMPLATES -->
  <xsl:apply-templates/>
  <!--                 -->
  <xsl:if test="@frame!='sides' and @frame!='none' and @frame!='top'">
   <xsl:text>\hline &#10;</xsl:text>
  </xsl:if>
  <xsl:text>\end{tabular}&#10;</xsl:text>
  <!-- <xsl:text>}</xsl:text> -->
 </xsl:template>
 

</xsl:stylesheet>

<!--
Local variables:
sgml-local-catalogs: ("catalog")
sgml-default-dtd-file: "../../src/xslt/xsl.ced"
End:
-->

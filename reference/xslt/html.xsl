<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>

 <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/html/docbook.xsl"/>
 <xsl:import
 href="http://docbook.sourceforge.net/release/xsl/snapshot/html/chunk-common.xsl"/>
 <xsl:import href="common.xsl"/>
 <xsl:import href="citation.xsl"/>
 <xsl:import href="biblio.xsl"/> 
 <xsl:include href="http://docbook.sourceforge.net/release/xsl/snapshot/html/manifest.xsl"/>
 <xsl:include href="http://docbook.sourceforge.net/release/xsl/snapshot/html/chunk-code.xsl"/>


 <xsl:output method="html" encoding="ISO-8859-1"
  doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN"
  doctype-system="http://www.w3.org/TR/html4/loose.dtd" indent="no"/>

 <!-- generate an HTML manifest -->
 <xsl:param name="generate.manifest" select="1"/>

 <!-- set some HTML-specific things, style sheet etc. -->
 <xsl:param name="html.stylesheet" doc:type="string">style.css</xsl:param>
 <xsl:param name="make.valid.html" select="1"/> 
 <xsl:param name="html.cleanup" select="1"/> 
 <xsl:param name="ignore.image.scaling" select="'1'"/>
 <xsl:param name="use.id.as.filename" select="1"/>

 <!-- crank up nominal image width from 6 * to 9 * -->
 <xsl:param name="nominal.image.width" select="9 * $pixels.per.inch"/>

 <xsl:param name="callout.list.table" select="'1'"/>
 <xsl:param name="callout.unicode" select="'1'"/>
 <xsl:param name="callout.graphics" select="'0'"/>

 <xsl:param name="profiling-highlighting" select="0"/>

 <xsl:param name="generate.toc">
appendix  nop
article/appendix  nop
article   toc,title
book      toc,title,figure,table,example,equation
chapter   toc,title
part      toc,title
preface   toc,title
qandadiv  toc
qandaset  toc
reference toc,title
sect1     toc
sect2     toc
sect3     toc
sect4     toc
sect5     toc
section   toc
set       toc,title
</xsl:param>

 <xsl:template match="pubdate" mode="book.titlepage.recto.auto.mode">
  <div xsl:use-attribute-sets="book.titlepage.recto.style">
   <xsl:apply-templates select="." mode="book.titlepage.recto.mode"/>
   <xsl:if test="$profiling-highlighting">
   <p><font color="blue">Blue</font> and <font color="green">green</font> text: common to 'anthro' book and main text.</p>
   <p><font color="red">Red</font> text: only 'anthro' book.</p>
  </xsl:if>
  </div>
 </xsl:template>

 <xsl:template match="varname">
  <xsl:call-template name="inline.italicmonoseq"/>
 </xsl:template>

 <xsl:template match="application">
  <xsl:call-template name="inline.monoseq"/>
 </xsl:template>

 <xsl:template match="phrase[@role='strong']">
  <xsl:call-template name="inline.boldseq"/>
 </xsl:template>

 <!-- override to get profile highlighting working properly -->

<!--
 <xsl:template match="para">
  <xsl:variable name="p">
   <p>

    <xsl:if test="position() = 1 and parent::listitem">
     <xsl:call-template name="anchor">
      <xsl:with-param name="node" select="parent::listitem"/>
     </xsl:call-template>
    </xsl:if>
    
    <xsl:call-template name="anchor"/>

    <xsl:choose>
     <xsl:when test="$profiling-highlighting">
      <xsl:choose>
       <xsl:when test="ancestor-or-self::*[@condition='anthro-book']">
        <font color="red"><xsl:apply-templates/></font>
      </xsl:when>
      <xsl:when test="ancestor-or-self::*[contains(@condition,'anthro-book')]">
        <font color="blue"><xsl:apply-templates/></font>
      </xsl:when>
      <xsl:when test="not(ancestor-or-self::*[@condition])">
        <font color="green"><xsl:apply-templates/></font>
      </xsl:when>
      <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
     </xsl:choose>
     </xsl:when>
    <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
    </xsl:choose>

   </p>

  </xsl:variable>

  <xsl:choose>
   <xsl:when test="$html.cleanup != 0">
    <xsl:call-template name="unwrap.p">
     <xsl:with-param name="p" select="$p"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <xsl:copy-of select="$p"/>
   </xsl:otherwise>
  </xsl:choose>
  
 </xsl:template>

 <xsl:template match="formalpara/para">
  <xsl:apply-imports/>
 </xsl:template>

 <xsl:template match="footnote/para[1]|footnote/simpara[1]" priority="2">
  <xsl:apply-imports/>
 </xsl:template>
-->

 <xsl:template match="article/appendix">
  <div class="{name(.)}">
   <xsl:if test="$generate.id.attributes != 0">
    <xsl:attribute name="id">
     <xsl:call-template name="object.id"/>
    </xsl:attribute>
   </xsl:if>
   
   <xsl:call-template name="section.heading">
    <xsl:with-param name="level" select="2"/>
    <xsl:with-param name="title">
     <xsl:apply-templates select="." mode="object.title.markup"/>
    </xsl:with-param>
   </xsl:call-template>
   
   <xsl:apply-templates select="appendixinfo" mode="appendix.titlepage.recto.auto.mode"/>
   
   <xsl:apply-templates/>
  </div>
 </xsl:template>

<!--  this customization should no longer be required as of 1.61.2
 <xsl:template name="head.content">
  <xsl:param name="node" select="."/>
  
  <title>
   <xsl:apply-templates select="$node" mode="object.title.markup.textonly"/>
  </title>
  
  <xsl:if test="$html.stylesheet">
   <link rel="stylesheet"
    href="{$html.stylesheet}"
    type="{$html.stylesheet.type}"/>
  </xsl:if>
  
  <xsl:if test="$link.mailto.url != ''">
   <link rev="made"
    href="{$link.mailto.url}"/>
  </xsl:if>
  
  <xsl:if test="$html.base != ''">
   <base href="{$html.base}"/>
  </xsl:if>
  
  <meta name="generator" content="DocBook XSL Stylesheets V{$VERSION}"/>
  
  <xsl:if test="ancestor-or-self::*[@status][1]/@status = 'draft'
   and $draft.watermark.image != ''">
   <style type="text/css"><xsl:text disable-output-escaping="yes">
     body { background-image: url("</xsl:text>
    <xsl:value-of select="$draft.watermark.image"/><xsl:text disable-output-escaping="yes">");
     background-repeat: no-repeat;
       background-position: top left;
     /* The following properties make the watermark "fixed" on the page. */
     /* I think that's just a bit too distracting for the reader... */
     /* background-attachment: fixed; */
     /* background-position: center center; */
    </xsl:text>
   </style>
  </xsl:if>
  <xsl:apply-templates select="." mode="head.keywords.content"/>
 </xsl:template>
-->

</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-indent-step: 1
sgml-indent-data: 1
sgml-default-dtd-file: "../../src/xslt/xsl.ced"
sgml-local-catalogs: ("catalog")
End:
-->

<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>
 
 <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/html/docbook.xsl"/>
 
 <xsl:param name="html.stylesheet" doc:type="string">style.css</xsl:param>
 <xsl:param name="make.valid.html" select="1"/>
 <xsl:param name="shade.verbatim" select="1"/>

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

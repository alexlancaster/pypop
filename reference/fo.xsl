<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

  <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/fo/docbook.xsl"/>

 <xsl:param name="page.margin.top">0.0in</xsl:param>
 <xsl:param name="page.margin.bottom">0.20in</xsl:param>
 <xsl:param name="page.margin.inner">0.60in</xsl:param>
 <xsl:param name="page.margin.outer">0.70in</xsl:param>
 <xsl:param name="body.margin.top">0.0in</xsl:param>
 <xsl:param name="body.margin.bottom">0.0in</xsl:param>
 <xsl:param name="body.font.family">Helvetica</xsl:param>
 <xsl:param name="title.margin.left" select="'-2pc'"/>
 <xsl:param name="toc.indent.width" select="8"/>
 <xsl:param name="insert.xref.page.number" select="1"/>

 <xsl:template match="phrase[@role='strong']">
  <xsl:call-template name="inline.boldseq"/>
 </xsl:template>

 <xsl:template match="article/appendix">
  <xsl:variable name="id">
   <xsl:call-template name="object.id"/>
  </xsl:variable>
  
  <fo:block id='{$id}'>

   <fo:block xmlns:fo="http://www.w3.org/1999/XSL/Format" xsl:use-attribute-sets="appendix.titlepage.recto.style" margin-left="{$title.margin.left}" font-size="17.28pt" font-weight="bold" font-family="{$title.font.family}">

   <xsl:call-template name="component.title">
    <xsl:with-param name="node" select="."/>
   </xsl:call-template>
   </fo:block>

   <!-- generate authorgroup -->

   <xsl:for-each select="appendixinfo/authorgroup/author">
    <xsl:apply-templates select="." mode="appendix.titlepage.recto.auto.mode"/>
   </xsl:for-each>
   <xsl:apply-templates/>

  </fo:block>
 
 </xsl:template>
 
 <!-- override the current rule, somehow duplicates the id for the
 containing block, this is fixed in docbook CVS -->

<!--
 <xsl:template match="glossentry">
  <xsl:variable name="id">
   <xsl:call-template name="object.id"/>
  </xsl:variable>
  
  <fo:list-item xsl:use-attribute-sets="normal.para.spacing">
   <xsl:call-template name="anchor">
    <xsl:with-param name="conditional">
     <xsl:choose>
      <xsl:when test="$glossterm.auto.link != 0
       or $glossary.collection != ''">0</xsl:when>
      <xsl:otherwise>1</xsl:otherwise>
     </xsl:choose>
    </xsl:with-param>
   </xsl:call-template>
   <xsl:apply-templates/>
  </fo:list-item>
 </xsl:template>

 <xsl:template match="glossentry/glossterm">
  <fo:list-item-label end-indent="label-end()">
   <fo:block>
      <xsl:apply-templates/>
   </fo:block>
  </fo:list-item-label>
 </xsl:template>
-->

</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-local-catalogs: ("catalog")
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->

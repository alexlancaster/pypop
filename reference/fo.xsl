<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

  <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/fo/docbook.xsl"/>

  <xsl:param name="page.margin.top">0.50in</xsl:param>
  <xsl:param name="page.margin.bottom">0.50in</xsl:param>
  <xsl:param name="page.margin.inner">0.60in</xsl:param>
  <xsl:param name="page.margin.outer">0.70in</xsl:param>
  <xsl:param name="body.font.family">Helvetica</xsl:param>
  <xsl:param name="title.margin.left" select="'-2pc'"/>
  <xsl:param name="insert.xref.page.number" doc:type="boolean">1</xsl:param>

  <xsl:template match="article/appendix">
   <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
   </xsl:variable>

   <fo:block id='{$id}'>
    <xsl:call-template name="section.heading">
      <xsl:with-param name="level" select="2"/>
      <xsl:with-param name="title">
        <!-- fix mode 'title.markup' to 'object.title.markup'. -->
        <xsl:apply-templates select="." mode="object.title.markup"/>
      </xsl:with-param>
      </xsl:call-template>

      <xsl:for-each select="appendixinfo/authorgroup/author">
       <xsl:apply-templates select="." mode="appendix.titlepage.recto.auto.mode"/>
      </xsl:for-each>

    <xsl:apply-templates/>
   </fo:block>
  </xsl:template>

  <!-- make a matching template for sections within appendices in
  articles to mirror the modified article/appendix rule above.
 -->
  <xsl:template match="article/appendix/section">
    <xsl:variable name="id">
     <xsl:call-template name="object.id"/>
    </xsl:variable>

   <fo:block id='{$id}'>
     <xsl:call-template name="section.heading">
       <xsl:with-param name="level" select="3"/>
       <xsl:with-param name="title">
         <xsl:apply-templates select="." mode="object.title.markup"/>
       </xsl:with-param>
     </xsl:call-template>

    <xsl:apply-templates/>
 
   </fo:block>
  </xsl:template>

 <!-- override the current rule, somehow duplicates the id for the
 containing block, this is fixed in docbook CVS -->

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

</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-local-catalogs: ("catalog")
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->

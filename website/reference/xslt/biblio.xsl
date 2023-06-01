<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

 <!-- top level templates that do the switch between html & FO -->
 <!-- depending on which stylesheet is being used -->

 <xsl:template match="bibliography">
  <xsl:choose>
   <xsl:when test="$stylesheet.result.type='html'">
    <xsl:apply-templates select="." mode="html"/>
   </xsl:when>
   <xsl:when test="$stylesheet.result.type='fo'">
    <xsl:apply-templates select="." mode="fo"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:message>Stylesheet type: <xsl:value-of select="$stylesheet.result.type"/> not recognized</xsl:message>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <xsl:template match="biblioentry">
  <xsl:choose>
   <xsl:when test="$stylesheet.result.type='html'">
    <xsl:apply-templates select="." mode="html"/>
   </xsl:when>
   <xsl:when test="$stylesheet.result.type='fo'">
    <xsl:apply-templates select="." mode="fo"/>
   </xsl:when>
  </xsl:choose>
 </xsl:template>

 <!-- ################################## -->
 <!--            BEGIN COMMON            -->
 <!-- ################################## -->

 <xsl:template name="order-biblioitems">
  <xsl:param name="bibitems"/>
  
  <xsl:apply-templates select="$bibitems">
   <xsl:sort select="@id"/>
   <xsl:sort select="abbrev"/>
   <xsl:sort select="@xreflabel"/>
  </xsl:apply-templates>
 </xsl:template>

 <xsl:template name="do-bibitems">

  <!-- do everythingg *except* for biblioentry, bibliomixed and bibliodivs -->
  <xsl:apply-templates select="*[not(self::biblioentry | self::bibliomixed | self::bibliodiv)]"/>
  
  <!-- if biblio* exist at this level, do them -->
   <xsl:if test="biblioentry|bibliomixed">
    <xsl:call-template name="order-biblioitems">
     <xsl:with-param name="bibitems" select="biblioentry|bibliomixed"/>
    </xsl:call-template>
   </xsl:if>
   
  <!-- bibliodivs are special because they can contain biblio* -->
  <xsl:if test="bibliodiv">
   <xsl:for-each select="bibliodiv">
    <xsl:choose>

     <!--  BEGIN HTML -->
     <xsl:when test="$stylesheet.result.type='html'">
      <!-- print div section -->
      <div class="{name(.)}">
       <!-- print title -->
       <h3 class="{name(title)}">
	<xsl:call-template name="anchor">
	 <xsl:with-param name="node" select="."/>
	</xsl:call-template>
       </h3>
       <!-- call current template recursively -->
       <xsl:call-template name="do-bibitems"/>
      </div>
     </xsl:when>
     <!--  END HTML -->

     <!--  BEGIN FO -->
     <xsl:when test="$stylesheet.result.type='fo'">
      <!-- generate fo block -->
      <fo:block>
       <xsl:attribute name="id">
	<xsl:call-template name="object.id"/>
       </xsl:attribute>
       <!-- make title -->
       <xsl:call-template name="bibliodiv.titlepage"/>
       <!-- call current template recursively -->
       <xsl:call-template name="do-bibitems"/>
      </fo:block>    
     </xsl:when>
     <!--  END FO -->

    </xsl:choose>

   </xsl:for-each>
   </xsl:if>
 </xsl:template>

 <!-- ################################## -->
 <!--            END COMMON              -->
 <!-- ################################## -->


 <!-- ################################## -->
 <!--            BEGIN HTML              -->
 <!-- ################################## -->

 <xsl:template match="bibliography" mode="html">
  <div class="{name(.)}">
   <xsl:if test="$generate.id.attributes != 0">
    <xsl:attribute name="id">
     <xsl:call-template name="object.id"/>
    </xsl:attribute>
   </xsl:if>
   
   <xsl:call-template name="bibliography.titlepage"/>

   <xsl:call-template name="do-bibitems"/>
   
   <xsl:call-template name="process.footnotes"/>
  </div>
 </xsl:template>

 <xsl:template match="biblioentry" mode="html">
  <xsl:variable name="id">
   <xsl:call-template name="object.id"/>
  </xsl:variable>

  <xsl:choose>
   <xsl:when test="string(.) = ''">
    <xsl:variable name="bib" select="document($bibliography.collection)"/>
    <xsl:variable name="entry" select="$bib/bibliography/*[@id=$id][1]"/>
    <xsl:choose>
     <xsl:when test="$entry">
      <xsl:apply-templates select="$entry"/>
     </xsl:when>
     <xsl:otherwise>
      <xsl:message>
       <xsl:text>No bibliography entry: </xsl:text>
       <xsl:value-of select="$id"/>
       <xsl:text> found in </xsl:text>
       <xsl:value-of select="$bibliography.collection"/>
      </xsl:message>
      <div class="{name(.)}">
       <xsl:call-template name="anchor"/>
       <p>
	<xsl:call-template name="biblioentry.label"/>
	<xsl:text>Error: no bibliography entry: </xsl:text>
	<xsl:value-of select="$id"/>
	<xsl:text> found in </xsl:text>
	<xsl:value-of select="$bibliography.collection"/>
       </p>
      </div>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:when>
   <xsl:otherwise>
    <xsl:variable name="bibid" select="@id"/>
    <xsl:variable name="ab" select="abbrev"/>
    <xsl:variable name="nx" select="//xref[@linkend=$bibid]"/>
    <xsl:variable name="nc" select="//citation[text()=$ab]"/>
    <xsl:variable name="ni" select="//citation[text()=$bibid]"/>

    <!-- only if cited, do we output reference -->
    <xsl:choose>
     <xsl:when test="count($nx) &gt; 0 or count($nc) &gt; 0 or count($ni) &gt; 0">
      <div class="{name(.)}">
       <xsl:call-template name="anchor"/>
       <p>
	<xsl:call-template name="biblioentry.label"/>
	<xsl:apply-templates mode="bibliography.mode"/>
       </p>
      </div>
     </xsl:when>
     <xsl:otherwise>
      <xsl:message>Entry: <xsl:value-of select="$id"/> in bibliography but not cited</xsl:message>
     </xsl:otherwise>
    </xsl:choose>

   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- ################################## -->
 <!--            END HTML                -->
 <!-- ################################## -->

 <!-- ################################## -->
 <!--            BEGIN FO                -->
 <!-- ################################## -->

 <xsl:template match="bibliography" mode="fo">
  <xsl:variable name="id">
   <xsl:call-template name="object.id"/>
  </xsl:variable>

  <xsl:choose>
   <xsl:when test="not(parent::*) or parent::book">
    <xsl:variable name="master-reference">
     <xsl:call-template name="select.pagemaster"/>
    </xsl:variable>
    
    <fo:page-sequence hyphenate="{$hyphenate}"
     master-reference="{$master-reference}">
     <xsl:attribute name="language">
      <xsl:call-template name="l10n.language"/>
     </xsl:attribute>
        <xsl:attribute name="format">
      <xsl:call-template name="page.number.format"/>
     </xsl:attribute>
     <xsl:if test="$double.sided != 0">
      <xsl:attribute name="initial-page-number">auto-odd</xsl:attribute>
     </xsl:if>
     <xsl:attribute name="hyphenation-character">
      <xsl:call-template name="gentext">
       <xsl:with-param name="key" select="'hyphenation-character'"/>
      </xsl:call-template>
     </xsl:attribute>
     <xsl:attribute name="hyphenation-push-character-count">
      <xsl:call-template name="gentext">
       <xsl:with-param name="key" select="'hyphenation-push-character-count'"/>
      </xsl:call-template>
     </xsl:attribute>
     <xsl:attribute name="hyphenation-remain-character-count">
      <xsl:call-template name="gentext">
       <xsl:with-param name="key" select="'hyphenation-remain-character-count'"/>
      </xsl:call-template>
     </xsl:attribute>
     
     <xsl:apply-templates select="." mode="running.head.mode">
      <xsl:with-param name="master-reference" select="$master-reference"/>
     </xsl:apply-templates>
     <xsl:apply-templates select="." mode="running.foot.mode">
      <xsl:with-param name="master-reference" select="$master-reference"/>
     </xsl:apply-templates>
     
     <fo:flow flow-name="xsl-region-body">
      <fo:block id="{$id}">
       <xsl:call-template name="bibliography.titlepage"/>
      </fo:block>

      <xsl:call-template name="do-bibitems"/>
      
      <!-- <xsl:apply-templates/> -->

     </fo:flow>
    </fo:page-sequence>
   </xsl:when>
   <xsl:otherwise>
    <fo:block id="{$id}"
     space-before.minimum="1em"
     space-before.optimum="1.5em"
     space-before.maximum="2em">
     <xsl:call-template name="bibliography.titlepage"/>
    </fo:block>
    
    <xsl:call-template name="do-bibitems"/>
    
   <!--     <xsl:apply-templates/>  -->
    
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <xsl:template match="biblioentry" mode="fo">
  <xsl:variable name="id"><xsl:call-template name="object.id"/></xsl:variable>
  <xsl:choose>
   <xsl:when test="string(.) = ''">
    <xsl:variable name="bib" select="document($bibliography.collection)"/>
    <xsl:variable name="entry" select="$bib/bibliography/*[@id=$id][1]"/>
    <xsl:choose>
     <xsl:when test="$entry">
      <xsl:apply-templates select="$entry"/>
     </xsl:when>
     <xsl:otherwise>
      <xsl:message>
       <xsl:text>No bibliography entry: </xsl:text>
       <xsl:value-of select="$id"/>
       <xsl:text> found in </xsl:text>
       <xsl:value-of select="$bibliography.collection"/>
      </xsl:message>
      <fo:block id="{$id}" xsl:use-attribute-sets="normal.para.spacing">
       <xsl:text>Error: no bibliography entry: </xsl:text>
       <xsl:value-of select="$id"/>
       <xsl:text> found in </xsl:text>
       <xsl:value-of select="$bibliography.collection"/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:when>

   <xsl:otherwise>
    <xsl:variable name="bibid" select="@id"/>
    <xsl:variable name="ab" select="abbrev"/>
    <xsl:variable name="nx" select="//xref[@linkend=$bibid]"/>
    <xsl:variable name="nc" select="//citation[text()=$ab]"/>
    <xsl:variable name="ni" select="//citation[text()=$bibid]"/>

    <!-- only if cited, do we output reference -->
    <xsl:choose>
     <xsl:when test="count($nx) &gt; 0 or count($nc) &gt; 0 or count($ni) &gt; 0">
      <fo:block id="{$id}" xsl:use-attribute-sets="normal.para.spacing"
       start-indent="0.5in" text-indent="-0.5in">
       <xsl:call-template name="biblioentry.label"/>
       <xsl:apply-templates mode="bibliography.mode"/>
      </fo:block>

     </xsl:when>
     <xsl:otherwise>
      <xsl:message>Entry: <xsl:value-of select="$id"/> in bibliography but not cited</xsl:message>
     </xsl:otherwise>
    </xsl:choose>

   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- ################################## -->
 <!--            END FO                  -->
 <!-- ################################## -->

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
